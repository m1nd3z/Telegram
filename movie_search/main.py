import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import asyncio

# Import our custom modules
from search_engine import search_movie, test_site_connectivity
from sites_config import list_sites, enable_site, disable_site

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
load_dotenv()

# Constants
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMIN_IDS = os.getenv('ADMIN_IDS', '').split(',')

# All search functions are now in search_engine.py module

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search requests."""
    # Check if message is from a user (not from channel/group)
    if not update.effective_user:
        await update.message.reply_text("❌ Эта команда доступна только в личных сообщениях.")
        return
    
    if str(update.effective_user.id) not in ADMIN_IDS:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")
        return

    query = update.message.text
    if not query or len(query.strip()) < 2:
        await update.message.reply_text("⚠️ Пожалуйста, введите более длинный поисковый запрос.")
        return

    status_message = await update.message.reply_text(f"🔍 Ищу '{query}'...")
    
    try:
        results = await search_movie(query)
        
        if not results:
            await status_message.edit_text("😕 Ничего не найдено.")
            return

        # Split results into chunks if message is too long
        message = f"🎬 *{query}*\n\n"
        chunks = []
        current_chunk = message

        for idx, result in enumerate(results, 1):
            # Format title with year if available
            title_with_year = result['title']
            if result.get('year'):
                title_with_year += f" ({result['year']})"
            
            result_text = f"*{idx}.* [{title_with_year}]({result['url']})\n"
            result_text += f"📺 Источник: {result['site']}\n\n"
            
            # Telegram message limit is 4096 characters
            if len(current_chunk) + len(result_text) > 4000:
                chunks.append(current_chunk)
                current_chunk = result_text
            else:
                current_chunk += result_text

        if current_chunk:
            chunks.append(current_chunk)

        # Send all chunks
        for chunk in chunks:
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=chunk,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        await status_message.edit_text("✅ Результаты опубликованы в канал!")
        
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error processing search for '{query}': {error_msg}")
        await status_message.edit_text(f"❌ Произошла ошибка при поиске.\nПодробности: {error_msg[:100]}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    # Check if message is from a user (not from channel/group)
    if not update.effective_user:
        await update.message.reply_text("❌ Эта команда доступна только в личных сообщениях.")
        return
    
    if str(update.effective_user.id) in ADMIN_IDS:
        await update.message.reply_text(
            "👋 Привет! Отправь мне название фильма или сериала, "
            "и я найду его для тебя и опубликую результаты в канал."
        )
    else:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    # Check if message is from a user (not from channel/group)
    if not update.effective_user:
        await update.message.reply_text("❌ Эта команда доступна только в личных сообщениях.")
        return
    
    if str(update.effective_user.id) in ADMIN_IDS:
        help_text = """
🔍 *Доступные команды:*

/search <запрос> - Поиск фильмов
/sites - Показать статус сайтов
/status - Проверить подключение к сайтам
/help - Показать эту справку

*Или просто отправьте название фильма/сериала для поиска.*
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")

async def sites_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /sites command."""
    # Check if message is from a user (not from channel/group)
    if not update.effective_user:
        await update.message.reply_text("❌ Эта команда доступна только в личных сообщениях.")
        return
    
    if str(update.effective_user.id) in ADMIN_IDS:
        sites_info = list_sites()
        message = "🌐 *Статус сайтов:*\n\n" + "\n".join(sites_info)
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command."""
    # Check if message is from a user (not from channel/group)
    if not update.effective_user:
        await update.message.reply_text("❌ Эта команда доступна только в личных сообщениях.")
        return
    
    if str(update.effective_user.id) in ADMIN_IDS:
        status_message = await update.message.reply_text("🔍 Проверяю подключение к сайтам...")
        
        try:
            connectivity_results = await test_site_connectivity()
            message = "🌐 *Статус подключения:*\n\n"
            for site, status in connectivity_results.items():
                message += f"• {site}: {status}\n"
            
            await status_message.edit_text(message, parse_mode='Markdown')
        except Exception as e:
            await status_message.edit_text(f"❌ Ошибка при проверке статуса: {str(e)}")
    else:
        await update.message.reply_text("❌ У вас нет доступа к этому боту.")

def main():
    """Start the bot."""
    if not all([TOKEN, CHANNEL_ID]):
        logging.error("Missing required environment variables. Check your .env file.")
        return

    try:
        # Create application
        application = Application.builder().token(TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("sites", sites_command))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))

        logging.info("Starting bot...")

        async def start_bot():
            # Verify channel access
            try:
                await application.bot.send_chat_action(chat_id=CHANNEL_ID, action="typing")
                logging.info("Channel verification successful")
            except Exception as e:
                logging.error(f"Channel verification failed: {str(e)}")
                logging.error(f"Bot cannot access channel {CHANNEL_ID}. Please check:")
                logging.error("1. Bot is added to the channel as an administrator")
                logging.error("2. Channel ID is correct")
                logging.error("3. Channel ID includes -100 prefix for supergroups/channels")
                return

            # Start polling
            await application.initialize()
            await application.start()
            await application.updater.start_polling()
            
            # Keep the application running
            while True:
                try:
                    await asyncio.sleep(1)
                except asyncio.CancelledError:
                    break

            # Cleanup
            await application.stop()

        # Run everything in asyncio
        asyncio.run(start_bot())

    except Exception as e:
        logging.error(f"Error starting bot: {str(e)}")
        raise e

if __name__ == '__main__':
    main()

"""
Search engine module for the Telegram bot.
Handles movie searching across multiple websites.
"""

import logging
import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from sites_config import get_enabled_sites

# Configure logging
logger = logging.getLogger(__name__)

# Constants
REQUEST_TIMEOUT = 30  # Increased timeout for PythonAnywhere
MAX_RETRIES = 2  # Reduced retries

def extract_year_from_title(title: str) -> tuple[str, str]:
    """
    Extract year from movie title and return clean title and year.
    Returns (clean_title, year) where year can be empty string if not found.
    """
    # Common year patterns in movie titles
    year_patterns = [
        r'\((\d{4})\)',  # (2023)
        r'\[(\d{4})\]',  # [2023]
        r'(\d{4})',      # 2023
        r'\((\d{4})\)\s*$',  # (2023) at end
        r'\[(\d{4})\]\s*$',  # [2023] at end
        r'(\d{4})\s*$',      # 2023 at end
    ]
    
    clean_title = title.strip()
    year = ""
    
    for pattern in year_patterns:
        match = re.search(pattern, clean_title)
        if match:
            year = match.group(1)
            # Remove the year from the title
            clean_title = re.sub(pattern, '', clean_title).strip()
            # Clean up extra spaces and punctuation
            clean_title = re.sub(r'\s+', ' ', clean_title)
            clean_title = re.sub(r'^\s*[\(\[\]\s]*\s*', '', clean_title)
            clean_title = re.sub(r'\s*[\(\[\]\s]*\s*$', '', clean_title)
            break
    
    return clean_title, year

def is_exact_title_match(query: str, title: str) -> bool:
    """
    Check if the title is an exact match for the query.
    Compares normalized versions of both strings.
    """
    # Normalize both strings
    def normalize_text(text: str) -> str:
        # Convert to lowercase
        text = text.lower()
        # Remove common punctuation and extra spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    query_norm = normalize_text(query)
    title_norm = normalize_text(title)
    
    # Check for exact match
    if query_norm == title_norm:
        return True
    
    # Check if query is contained in title (for partial matches)
    if query_norm in title_norm:
        return True
    
    # Check if all query words are present in title
    query_words = query_norm.split()
    title_words = title_norm.split()
    
    # All query words must be present in title
    return all(word in title_words for word in query_words)

def prepare_search_query(query: str) -> str:
    """Prepare search query for exact matching."""
    # Remove extra spaces and trim
    query = ' '.join(query.split())
    # Remove quotes as they're added in the search pattern
    query = query.replace('"', '')
    # Escape special characters
    query = quote(query)
    return query

def prepare_search_query_alternative(query: str) -> str:
    """Prepare search query with alternative encoding."""
    # Remove extra spaces and trim
    query = ' '.join(query.split())
    # Remove quotes as they're added in the search pattern
    query = query.replace('"', '')
    # Use different encoding approach
    return query.replace(' ', '+')

async def fetch_with_retry(session: aiohttp.ClientSession, url: str, headers: dict, timeout: int = REQUEST_TIMEOUT) -> tuple[bool, str]:
    """Fetch URL with retry logic - optimized for PythonAnywhere."""
    for attempt in range(MAX_RETRIES):
        try:
            # Use SSL=True for PythonAnywhere
            async with session.get(url, headers=headers, ssl=True, timeout=timeout) as response:
                if response.status == 200:
                    # Fix encoding issues for PythonAnywhere
                    try:
                        content = await response.text(encoding='utf-8')
                        return True, content
                    except UnicodeDecodeError:
                        # Fallback to different encoding
                        content = await response.read()
                        try:
                            return True, content.decode('utf-8', errors='ignore')
                        except:
                            return True, content.decode('latin-1', errors='ignore')
                logger.warning(f"Attempt {attempt + 1} failed for {url}: Status {response.status}")
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
        if attempt < MAX_RETRIES - 1:
            await asyncio.sleep(2)  # Increased wait time
    return False, ""

async def search_site(session: aiohttp.ClientSession, site_name: str, site_config: dict, query: str, headers: dict) -> list[dict]:
    """Search a single site for movies."""
    results = []
    site_url = site_config['url']
    prepared_query = prepare_search_query(query)
    timeout = site_config.get('timeout', REQUEST_TIMEOUT)
    max_results = site_config.get('max_results', 5)
    
    # Try main search pattern first
    search_patterns = [site_config['search_pattern']]
    
    # Add alternative patterns if available
    if 'alternative_patterns' in site_config:
        search_patterns.extend(site_config['alternative_patterns'])
    
    # Try both query encoding methods
    query_variants = [prepared_query]
    # Try alternative encoding for all sites
    query_variants.append(prepare_search_query_alternative(query))
    
    for pattern in search_patterns:
        for query_variant in query_variants:
            search_url = site_url + pattern.format(query=query_variant)
            
            try:
                logger.info(f"Searching {site_name} ({site_url}) for '{query}' using pattern: {pattern} with query: {query_variant}")
                success, html = await fetch_with_retry(session, search_url, headers, timeout)
                
                if success:
                    soup = BeautifulSoup(html, 'html.parser')
                    logger.debug(f"HTML content length for {site_name}: {len(html)}")
                    
                    # Try to find movie items using all selectors
                    items = []
                    for selector in site_config['selectors']:
                        found_items = soup.select(selector)
                        logger.info(f"Found {len(found_items)} items matching selector '{selector}' on {site_name}")
                        items.extend(found_items)
                    
                    # Also try to find any links that might contain movie URLs
                    movie_links = soup.find_all('a', href=True)
                    for link in movie_links:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        # More lenient - include any link with text that might be a movie title
                        if (any(keyword in href.lower() for keyword in ['/film/', '/serial/', '/movie/', '/video/']) or
                            (text and len(text) > 2 and not text.isdigit() and not text.startswith('http'))):
                            items.append(link)
                    
                    # Remove duplicates while preserving order
                    seen_items = set()
                    unique_items = []
                    for item in items:
                        item_str = str(item)
                        if item_str not in seen_items:
                            seen_items.add(item_str)
                            unique_items.append(item)
                    
                    # Process found items
                    for item in unique_items:
                        # Try different ways to get title and URL
                        link = item
                        if item.name != 'a':
                            link = item.find('a')
                            if not link:
                                link = item.parent.find('a') if item.parent else None
                        
                        if link and link.name == 'a':
                            title = (link.get('title', '') or 
                                    link.text.strip() or 
                                    item.get_text(strip=True))
                            url = link.get('href', '')
                            
                            if title and url and len(title.strip()) > 2:
                                # STRICT MATCHING: Only include results with exact title match
                                if not is_exact_title_match(query, title):
                                    continue  # Skip this result
                                
                                if not url.startswith('http'):
                                    url = site_url + ('/' if not url.startswith('/') else '') + url
                                
                                # Extract year from title
                                clean_title, year = extract_year_from_title(title)
                                
                                result = {
                                    'title': clean_title,
                                    'year': year,
                                    'url': url,
                                    'site': site_name,
                                    'site_url': site_url,
                                    'original_title': title  # Keep original for reference
                                }
                                
                                # Check if this result is not already in results
                                is_duplicate = any(r['url'] == result['url'] for r in results)
                                if not is_duplicate:
                                    results.append(result)
                                    logger.info(f"Found exact match on {site_name}: {clean_title} ({year})")
                    
                    # If we found results with this pattern, break out of the pattern loop
                    if results:
                        break
                else:
                    logger.warning(f"Failed to fetch content from {site_name} with pattern: {pattern}")
                    
            except Exception as e:
                logger.error(f"Error searching {site_name} with pattern {pattern}: {str(e)}")
                continue  # Try next pattern
        
        # If we found results, break out of the pattern loop
        if results:
            break
    
    return results[:max_results]  # Return only top results

async def search_movie(query: str) -> list[dict]:
    """Search for movies across all enabled sites."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }
    
    enabled_sites = get_enabled_sites()
    logger.info(f"Searching across {len(enabled_sites)} enabled sites: {list(enabled_sites.keys())}")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site_name, site_config in enabled_sites.items():
            tasks.append(search_site(session, site_name, site_config, query, headers))
        
        results = []
        for completed_task in await asyncio.gather(*tasks, return_exceptions=True):
            if isinstance(completed_task, list):
                results.extend(completed_task)
            elif isinstance(completed_task, Exception):
                logger.error(f"Task failed with exception: {completed_task}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_results = []
    for result in results:
        if result['url'] not in seen:
            seen.add(result['url'])
            unique_results.append(result)
    
    logger.info(f"Found {len(unique_results)} unique exact matches for '{query}' across all sites")
    return unique_results

async def test_site_connectivity():
    """Test connectivity to all enabled sites."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    enabled_sites = get_enabled_sites()
    results = {}
    
    async with aiohttp.ClientSession() as session:
        for site_name, site_config in enabled_sites.items():
            try:
                success, _ = await fetch_with_retry(session, site_config['url'], headers, 10)
                results[site_name] = "✅ Online" if success else "❌ Offline"
            except Exception as e:
                results[site_name] = f"❌ Error: {str(e)[:50]}"
    
    return results 
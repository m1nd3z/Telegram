
# 🎬 Movie Search Telegram Bot

Telegram botas, kuris ieško filmų ir serialų iš trijų populiarių rusiškų svetainių ir rezultatus siunčia į Telegram kanalą.

## �� Funkcijos

- 🔍 **Tikslus filmų paieškos** - rodo tik filmus su identiškais pavadinimais
- 📅 **Metų rodymas** - automatiškai ištraukia ir rodo filmo metus
- 🌐 **Ieško iš trijų svetainių vienu metu:**
  - kinogo.uk
  - kinokong.day  
  - gidonline.eu
- 📱 **Telegram integracija** - rezultatai siunčiami į kanalą
- 🔐 **Saugumas** - tik administratoriai gali naudoti botą
- ⚡ **Asinchroninis** - greitas paieška visuose svetainėse
- 🛠️ **Modulinis kodas** - lengvai plečiamas ir valdomas

## 📁 Projekto struktūra

```
movies/
├── main.py                    # Pagrindinis botas
├── search_engine.py           # Paieškos variklis su tiksliais atitikmenimis
├── sites_config.py            # Svetainių konfigūracija
├── test_strict_search.py      # Tikslaus paieškos testavimas
├── test_year_extraction.py    # Metų ištraukimo testavimas
├── requirements.txt           # Python bibliotekos
├── .env                       # Konfigūracija (sukurkite patys)
└── README.md                  # Šis failas
```

## 🚀 Instaliavimas

### 1. Klonuokite projektą
```bash
git clone <repository-url>
cd movies
```

### 2. Sukurkite virtual environment
```bash
python3 -m venv movies_venv
source movies_venv/bin/activate  # Linux/Mac
# arba
movies_venv\Scripts\activate.bat  # Windows
```

### 3. Įdėkite bibliotekas
```bash
pip install -r requirements.txt
```

### 4. Sukurkite .env failą
```bash
nano .env
```

Įdėkite šiuos duomenis:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here
ADMIN_IDS=your_telegram_user_id_here
```

## 🔧 Konfigūracija

### Telegram Bot Token
1. Eikite į @BotFather Telegram
2. Sukurkite naują botą: `/newbot`
3. Nukopijuokite token

### Kanalo ID
1. Pridėkite botą į kanalą kaip administratorių
2. Paleiskite botą ir išsiųskite žinutę į kanalą
3. Patikrinkite bot log'us arba naudokite Telegram API

### Administratoriaus ID
1. Parašykite @userinfobot Telegram
2. Nukopijuokite savo ID numerį

## 🧪 Testavimas

### Patikrinkite metų ištraukimą
```bash
python test_year_extraction.py
```

### Patikrinkite tikslų paiešką
```bash
python test_strict_search.py
```

## 🎯 Naudojimas

### Paleiskite botą
```bash
python main.py
```

### Telegram komandos
- `/start` - Pradėti
- `/help` - Pagalba
- `/sites` - Svetainių statusas
- `/status` - Patikrinti svetainių ryšį
- `<filmo pavadinimas>` - Ieškoti filmo

## ⚙️ Svetainių valdymas

### Pridėti naują svetainę
Redaguokite `sites_config.py`:

```python
SITES_CONFIG['naujas_svetaine.com'] = {
    'url': 'https://naujas_svetaine.com',
    'search_pattern': '/search?q={query}',
    'selectors': ['.movie-item', '.movie-title'],
    'enabled': True,
    'timeout': 15,
    'max_results': 5
}
```

### Išjungti svetainę
```python
from sites_config import disable_site
disable_site('kinogo.uk')
```

### Įjungti svetainę
```python
from sites_config import enable_site
enable_site('kinogo.uk')
```

## 🔍 Paieškos algoritmas

1. **Tikslus pavadinimų atitikimas** - tik filmai su identiškais pavadinimais
2. **Metų ištraukimas** - automatiškai ištraukia metus iš pavadinimų
3. **Užklausos paruošimas** - valymas ir kodavimas
4. **Lygiagreti paieška** - visuose svetainėse vienu metu
5. **HTML parsavimas** - BeautifulSoup naudojimas
6. **Dublikatų šalinimas** - unikalūs rezultatai

## 🎬 Rezultatų pavyzdys

```
🎬 Главы государств

1. Главы государств (2023)
   📺 Источник: kinogo.uk

2. Главы государств (2023)
   📺 Источник: kinokong.day
```

## 🛡️ Saugumas

- **Tik administratoriai** gali naudoti botą
- **SSL patikrinimas** išjungtas dėl svetainių problemų
- **Timeout** apsauga nuo lėtų svetainių
- **Retry logika** automatinis bandymas iš naujo

## 🐛 Problemų sprendimas

### Botas neveikia
1. Patikrinkite `.env` failą
2. Patikrinkite, ar botas pridėtas į kanalą
3. Patikrinkite interneto ryšį

### Neranda rezultatų
1. Paleiskite `python test_strict_search.py`
2. Patikrinkite svetainių statusą su `/status`
3. Pabandykite kitą paieškos užklausą

### Lėtas veikimas
1. Patikrinkite interneto greitį
2. Sumažinkite `timeout` reikšmes `sites_config.py`
3. Išjunkite nereikalingus svetainės

## 📝 Licencija

Šis projektas skirtas tik mokymosi tikslams.

## 🤝 Prisidėjimas

1. Fork'inkite projektą
2. Sukurkite feature branch
3. Commit'inkite pakeitimus
4. Push'inkite į branch
5. Sukurkite Pull Request

## 📞 Pagalba

Jei turite klausimų ar problemų:
1. Patikrinkite šį README
2. Paleiskite testavimo skriptus
3. Patikrinkite log failus 

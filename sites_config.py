"""
Movie sites configuration for the Telegram bot.
This file contains all the settings for different movie websites.
"""

# Movie sites configuration
SITES_CONFIG = {
    'kinogo.uk': {
        'url': 'https://kinogo.uk',
        'search_pattern': '/index.php?do=search&subaction=search&story={query}',
        'alternative_patterns': ['/search/?q={query}', '/search/{query}', '/?s={query}', '/index.php?do=search&subaction=search&story={query}&titleonly=3'],
        'selectors': ['.short-item', '.short-title', '.short-text', '.short-item a', '.short-item .short-title a', 'a[href*="/film/"]', 'a[href*="/serial/"]', '.short-item a', 'a[href*="/"]', '.item', '.item a', '.movie-item', '.movie-title', '.movie-link', '.movie-item a', '.movie-item .movie-title a', 'a[href*="/movie/"]', 'a[href*="/video/"]', '.mainlink', '.mqn', '.th-item a', '.th-item', '.mainlink a', 'a[href*="/"]'],
        'enabled': True,
        'timeout': 15,
        'max_results': 5
    },
    'kinokong.day': {
        'url': 'https://kinokong.day',
        'search_pattern': '/index.php?do=search&subaction=search&story={query}',
        'alternative_patterns': ['/search/?q={query}', '/search/{query}', '/?s={query}', '/index.php?do=search&subaction=search&story={query}&titleonly=3'],
        'selectors': ['.movie-item', '.movie-title', '.movie-link', '.movie-item a', '.movie-item .movie-title a', 'a[href*="/film/"]', 'a[href*="/serial/"]', '.movie-item a', 'a[href*="/"]', '.item', '.item a', '.short-item', '.short-title', '.short-text', '.short-item a', '.short-item .short-title a', 'a[href*="/movie/"]', 'a[href*="/video/"]', '.mainlink', '.mqn', '.th-item a', '.th-item', '.mainlink a', 'a[href*="/"]', 'a[href*="/94186"]', 'a[href*="/77303"]'],
        'enabled': True,
        'timeout': 15,
        'max_results': 5
    },
    'gidonline.eu': {
        'url': 'https://gidonline.eu',
        'search_pattern': '/index.php?do=search&subaction=search&story={query}',
        'alternative_patterns': ['/search/?q={query}', '/search/{query}', '/?s={query}', '/index.php?do=search&subaction=search&story={query}&titleonly=3'],
        'selectors': ['.mainlink', '.mqn', '.th-item a', '.th-item', 'a[href*="/film/"]', 'a[href*="/serial/"]', '.mainlink a', 'a[href*="/"]', '.short-item', '.short-title', '.short-text', '.short-item a', '.short-item .short-title a', '.movie-item', '.movie-title', '.movie-link', '.movie-item a', '.movie-item .movie-title a', 'a[href*="/movie/"]', 'a[href*="/video/"]', 'a[href*="/"]', '.item', '.item a', 'a[href*="/"]'],
        'enabled': True,
        'timeout': 15,
        'max_results': 5
    }
}

# Additional sites that can be easily added
ADDITIONAL_SITES = {
    'kinopoisk.ru': {
        'url': 'https://www.kinopoisk.ru',
        'search_pattern': '/index.php?kp_query={query}',
        'selectors': ['.film-item', '.film-title', '.film-link'],
        'enabled': False,  # Disabled by default
        'timeout': 15,
        'max_results': 5
    },
    'ivi.ru': {
        'url': 'https://www.ivi.ru',
        'search_pattern': '/search/?q={query}',
        'selectors': ['.movie-item', '.movie-title', '.movie-link'],
        'enabled': False,  # Disabled by default
        'timeout': 15,
        'max_results': 5
    }
}

def get_enabled_sites():
    """Get only enabled sites from configuration."""
    return {name: config for name, config in SITES_CONFIG.items() if config.get('enabled', True)}

def add_site(site_name: str, site_config: dict):
    """Add a new site to the configuration."""
    SITES_CONFIG[site_name] = site_config

def remove_site(site_name: str):
    """Remove a site from the configuration."""
    if site_name in SITES_CONFIG:
        del SITES_CONFIG[site_name]

def enable_site(site_name: str):
    """Enable a site in the configuration."""
    if site_name in SITES_CONFIG:
        SITES_CONFIG[site_name]['enabled'] = True

def disable_site(site_name: str):
    """Disable a site in the configuration."""
    if site_name in SITES_CONFIG:
        SITES_CONFIG[site_name]['enabled'] = False

def get_site_config(site_name: str):
    """Get configuration for a specific site."""
    return SITES_CONFIG.get(site_name)

def list_sites():
    """List all sites with their status."""
    sites_info = []
    for name, config in SITES_CONFIG.items():
        status = "✅ Enabled" if config.get('enabled', True) else "❌ Disabled"
        sites_info.append(f"{name}: {status}")
    return sites_info 
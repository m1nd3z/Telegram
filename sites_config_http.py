"""
Movie sites configuration with HTTP URLs for PythonAnywhere testing.
"""

# Movie sites configuration with HTTP
SITES_CONFIG_HTTP = {
    'kinogo.uk': {
        'url': 'http://kinogo.uk',
        'search_pattern': '/index.php?do=search&subaction=search&story={query}',
        'alternative_patterns': ['/search/?q={query}', '/search/{query}', '/?s={query}', '/index.php?do=search&subaction=search&story={query}&titleonly=3'],
        'selectors': ['.short-item', '.short-title', '.short-text', '.short-item a', '.short-item .short-title a', 'a[href*="/film/"]', 'a[href*="/serial/"]', '.short-item a', 'a[href*="/"]', '.item', '.item a', '.movie-item', '.movie-title', '.movie-link', '.movie-item a', '.movie-item .movie-title a', 'a[href*="/movie/"]', 'a[href*="/video/"]', '.mainlink', '.mqn', '.th-item a', '.th-item', '.mainlink a', 'a[href*="/"]'],
        'enabled': True,
        'timeout': 15,
        'max_results': 5
    },
    'kinokong.day': {
        'url': 'http://kinokong.day',
        'search_pattern': '/index.php?do=search&subaction=search&story={query}',
        'alternative_patterns': ['/search/?q={query}', '/search/{query}', '/?s={query}', '/index.php?do=search&subaction=search&story={query}&titleonly=3'],
        'selectors': ['.movie-item', '.movie-title', '.movie-link', '.movie-item a', '.movie-item .movie-title a', 'a[href*="/film/"]', 'a[href*="/serial/"]', '.movie-item a', 'a[href*="/"]', '.item', '.item a', '.short-item', '.short-title', '.short-text', '.short-item a', '.short-item .short-title a', 'a[href*="/movie/"]', 'a[href*="/video/"]', '.mainlink', '.mqn', '.th-item a', '.th-item', '.mainlink a', 'a[href*="/"]', 'a[href*="/94186"]', 'a[href*="/77303"]'],
        'enabled': True,
        'timeout': 15,
        'max_results': 5
    },
    'gidonline.eu': {
        'url': 'http://gidonline.eu',
        'search_pattern': '/index.php?do=search&subaction=search&story={query}',
        'alternative_patterns': ['/search/?q={query}', '/search/{query}', '/?s={query}', '/index.php?do=search&subaction=search&story={query}&titleonly=3'],
        'selectors': ['.mainlink', '.mqn', '.th-item a', '.th-item', 'a[href*="/film/"]', 'a[href*="/serial/"]', '.mainlink a', 'a[href*="/"]', '.short-item', '.short-title', '.short-text', '.short-item a', '.short-item .short-title a', '.movie-item', '.movie-title', '.movie-link', '.movie-item a', '.movie-item .movie-title a', 'a[href*="/movie/"]', 'a[href*="/video/"]', 'a[href*="/"]', '.item', '.item a', 'a[href*="/"]'],
        'enabled': True,
        'timeout': 15,
        'max_results': 5
    }
}

def get_enabled_sites_http():
    """Get only enabled sites from HTTP configuration."""
    return {name: config for name, config in SITES_CONFIG_HTTP.items() if config.get('enabled', True)} 
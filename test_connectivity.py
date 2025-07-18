#!/usr/bin/env python3
"""
Test svetainių prieinamumą iš PythonAnywhere.
"""

import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_site_connectivity():
    """Test svetainių prieinamumą."""
    
    sites = [
        'https://kinogo.uk',
        'https://kinokong.day', 
        'https://gidonline.eu',
        'https://www.google.com',  # Testui
        'https://httpbin.org/get'  # Testui
    ]
    
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
    
    print("🧪 Testing site connectivity from PythonAnywhere")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        for site in sites:
            print(f"\n🔍 Testing: {site}")
            try:
                # Try with SSL
                async with session.get(site, headers=headers, ssl=True, timeout=10) as response:
                    print(f"✅ SSL: Status {response.status}")
                    if response.status == 200:
                        content = await response.text()
                        print(f"   Content length: {len(content)} characters")
                    else:
                        print(f"   Error status: {response.status}")
            except Exception as e:
                print(f"❌ SSL Error: {str(e)[:100]}")
                
                # Try without SSL
                try:
                    async with session.get(site, headers=headers, ssl=False, timeout=10) as response:
                        print(f"✅ No SSL: Status {response.status}")
                        if response.status == 200:
                            content = await response.text()
                            print(f"   Content length: {len(content)} characters")
                        else:
                            print(f"   Error status: {response.status}")
                except Exception as e2:
                    print(f"❌ No SSL Error: {str(e2)[:100]}")
            
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_site_connectivity()) 
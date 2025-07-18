#!/usr/bin/env python3
"""
Test pataisytą paieškos variklį PythonAnywhere aplinkoje.
"""

import asyncio
import logging
from search_engine import search_movie

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_search():
    """Test paieškos funkcionalumą."""
    
    test_queries = [
        "Главы государств",
        "Интерстеллар",
        "Матрица"
    ]
    
    print("🧪 Testing Fixed Search Engine")
    print("=" * 40)
    
    for query in test_queries:
        print(f"\n🔍 Searching for: '{query}'")
        print("-" * 30)
        
        try:
            results = await search_movie(query)
            
            if not results:
                print("❌ No exact matches found")
            else:
                print(f"✅ Found {len(results)} exact matches:")
                for idx, result in enumerate(results, 1):
                    title_with_year = result['title']
                    if result.get('year'):
                        title_with_year += f" ({result['year']})"
                    
                    print(f"  {idx}. {title_with_year}")
                    print(f"     📺 Site: {result['site']}")
                    print(f"     🔗 URL: {result['url']}")
                    print()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            logger.error(f"Search failed for '{query}': {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_search()) 
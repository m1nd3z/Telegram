#!/usr/bin/env python3
"""
Test script for strict title matching and year extraction.
"""

import asyncio
import logging
from search_engine import search_movie, extract_year_from_title, is_exact_title_match

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_strict_search():
    """Test the strict search functionality."""
    
    # Test queries
    test_queries = [
        "Главы государств",
        "Интерстеллар",
        "Матрица",
        "Титаник",
        "Аватар"
    ]
    
    print("🧪 Testing Strict Search with Year Extraction")
    print("=" * 50)
    
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
                    if result.get('original_title') and result['original_title'] != result['title']:
                        print(f"     📝 Original: {result['original_title']}")
                    print()
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_year_extraction():
    """Test year extraction function."""
    print("\n🧪 Testing Year Extraction")
    print("=" * 30)
    
    test_titles = [
        "Главы государств (2023)",
        "Интерстеллар [2014]",
        "Матрица 1999",
        "Титаник (1997)",
        "Аватар 2009",
        "Фильм без года",
        "Другой фильм (2020) с дополнительным текстом",
        "Фильм [2021] в конце",
        "2022 Фильм в начале"
    ]
    
    for title in test_titles:
        clean_title, year = extract_year_from_title(title)
        print(f"Original: '{title}'")
        print(f"Clean: '{clean_title}' | Year: '{year}'")
        print("-" * 40)

def test_exact_matching():
    """Test exact title matching function."""
    print("\n🧪 Testing Exact Title Matching")
    print("=" * 35)
    
    test_cases = [
        ("Главы государств", "Главы государств (2023)", True),
        ("Главы государств", "Главы государств", True),
        ("Интерстеллар", "Интерстеллар [2014]", True),
        ("Матрица", "Матрица 1999", True),
        ("Титаник", "Титаник (1997)", True),
        ("Главы государств", "Другой фильм", False),
        ("Интерстеллар", "Интерстеллар 2", True),  # Partial match
        ("Матрица", "Матрица: Перезагрузка", True),  # Partial match
    ]
    
    for query, title, expected in test_cases:
        result = is_exact_title_match(query, title)
        status = "✅" if result == expected else "❌"
        print(f"{status} Query: '{query}' | Title: '{title}' | Expected: {expected} | Got: {result}")

async def main():
    """Run all tests."""
    print("🚀 Starting Strict Search Tests")
    print("=" * 50)
    
    # Test year extraction
    test_year_extraction()
    
    # Test exact matching
    test_exact_matching()
    
    # Test actual search
    await test_strict_search()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 
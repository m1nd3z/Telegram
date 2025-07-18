#!/usr/bin/env python3
"""
Simple test for year extraction function.
"""

from search_engine import extract_year_from_title

def test_year_extraction():
    """Test year extraction function."""
    print("🧪 Testing Year Extraction")
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

if __name__ == "__main__":
    test_year_extraction() 
#!/usr/bin/env python3
"""
Test script to verify scraper functionality.
Tests a few URLs from different platforms.
"""

from scraper import scrape_product

# Test URLs from different platforms
TEST_URLS = [
    {
        "name": "Shopify Store",
        "url": "https://melaniaclara.com/products/quinn-earrings-silver-clear"
    },
    {
        "name": "Etsy Product",
        "url": "https://www.etsy.com/listing/180164385/personalized-chinese-name-sterling"
    },
    {
        "name": "Nordstrom Product",
        "url": "https://www.nordstrom.com/s/zella-live-in-high-waist-leggings/3035756"
    }
]


def test_scraper():
    """Test scraper on sample URLs."""
    print("=" * 80)
    print("SCRAPER TEST")
    print("=" * 80)
    
    for test in TEST_URLS:
        print(f"\nTesting: {test['name']}")
        print(f"URL: {test['url']}")
        print("-" * 80)
        
        result = scrape_product(test['url'])
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Name: {result.get('name', 'N/A')}")
            print(f"💰 Current Price: ${result.get('current_price', 0):.2f}")
            
            if result.get('original_price'):
                print(f"📊 Original Price: ${result['original_price']:.2f}")
            
            if result.get('is_on_sale'):
                print(f"🔥 ON SALE: {result['discount_percent']}% off")
            else:
                print("📌 Regular Price")
        
        print()
    
    print("=" * 80)
    print("Test complete!")


if __name__ == '__main__':
    test_scraper()

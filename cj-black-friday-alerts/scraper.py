"""
Web scraper module for Black Friday price tracking.
Handles multiple e-commerce platforms with intelligent price extraction.
"""

import re
import time
import random
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# User agent rotation for avoiding blocks
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]


class ProductScraper:
    """Base scraper class with common functionality."""
    
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        
    def get_headers(self) -> Dict[str, str]:
        """Get random headers to avoid detection."""
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch page content with error handling.
        
        Args:
            url: Page URL
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            # Add random delay to be polite
            time.sleep(random.uniform(0.5, 2.0))
            
            response = self.session.get(
                url,
                headers=self.get_headers(),
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def parse_price(self, price_text: str) -> Optional[float]:
        """
        Parse price from text string.
        
        Args:
            price_text: Price string like "$19.99", "$1,999.00", "19.99"
            
        Returns:
            Float price or None if parsing failed
        """
        if not price_text:
            return None
            
        # Remove currency symbols, commas, and whitespace
        cleaned = re.sub(r'[^\d.]', '', price_text)
        
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    def calculate_discount(
        self,
        current_price: float,
        original_price: float
    ) -> Tuple[bool, float]:
        """
        Calculate if on sale and discount percentage.
        
        Args:
            current_price: Current price
            original_price: Original/compare-at price
            
        Returns:
            Tuple of (is_on_sale, discount_percent)
        """
        if not original_price or not current_price:
            return False, 0.0
            
        if current_price < original_price:
            discount = ((original_price - current_price) / original_price) * 100
            return True, round(discount, 2)
            
        return False, 0.0


class ShopifyScraper(ProductScraper):
    """Scraper for Shopify-based stores."""
    
    def scrape(self, url: str) -> Dict:
        """Scrape Shopify product page."""
        soup = self.fetch_page(url)
        
        if not soup:
            return {'error': 'Failed to fetch page'}
        
        result = {
            'name': None,
            'current_price': None,
            'original_price': None,
            'is_on_sale': False,
            'discount_percent': 0.0
        }
        
        # Extract product name
        name_selectors = [
            'h1.product-title',
            'h1.product__title',
            'h1[itemprop="name"]',
            '.product-single__title',
            'h1.product_name'
        ]
        
        for selector in name_selectors:
            name_elem = soup.select_one(selector)
            if name_elem:
                result['name'] = name_elem.get_text(strip=True)
                break
        
        # Extract prices - try JSON-LD first (most reliable)
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                import json
                data = json.loads(json_ld.string)
                if isinstance(data, list):
                    data = data[0]
                
                if 'offers' in data:
                    offer = data['offers']
                    if isinstance(offer, list):
                        offer = offer[0]
                    
                    result['current_price'] = float(offer.get('price', 0))
                    
                    # Check for original price
                    if 'priceSpecification' in offer:
                        result['original_price'] = float(
                            offer['priceSpecification'].get('price', 0)
                        )
            except Exception:
                pass
        
        # Fallback to HTML price selectors
        if not result['current_price']:
            price_selectors = [
                '.price__current .money',
                '.product-price .money',
                'span.price',
                '.product__price .money',
                '[data-product-price]',
                '.price-item--sale'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    result['current_price'] = self.parse_price(price_text)
                    if result['current_price']:
                        break
        
        # Look for compare-at (original) price
        if not result['original_price']:
            original_selectors = [
                '.price__compare .money',
                '.product__price--compare-at',
                '.price-item--regular',
                'del .money',
                's .money',
                '.was-price'
            ]
            
            for selector in original_selectors:
                orig_elem = soup.select_one(selector)
                if orig_elem:
                    price_text = orig_elem.get_text(strip=True)
                    result['original_price'] = self.parse_price(price_text)
                    if result['original_price']:
                        break
        
        # Calculate discount
        if result['current_price'] and result['original_price']:
            result['is_on_sale'], result['discount_percent'] = self.calculate_discount(
                result['current_price'],
                result['original_price']
            )
        
        return result


class EtsyScraper(ProductScraper):
    """Scraper for Etsy products."""
    
    def scrape(self, url: str) -> Dict:
        """Scrape Etsy product page."""
        soup = self.fetch_page(url)
        
        if not soup:
            return {'error': 'Failed to fetch page'}
        
        result = {
            'name': None,
            'current_price': None,
            'original_price': None,
            'is_on_sale': False,
            'discount_percent': 0.0
        }
        
        # Product name
        name_elem = soup.select_one('h1[data-listing-title]') or soup.select_one('h1.wt-text-body-01')
        if name_elem:
            result['name'] = name_elem.get_text(strip=True)
        
        # Current price
        price_selectors = [
            'div[data-buy-box-region="price"] p.wt-text-title-03',
            'p.wt-text-title-03[data-buy-box-region-price]',
            'div.price p.wt-text-title-03'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                result['current_price'] = self.parse_price(price_text)
                if result['current_price']:
                    break
        
        # Original price (if on sale)
        original_elem = soup.select_one('p.wt-text-strikethrough') or soup.select_one('del')
        if original_elem:
            price_text = original_elem.get_text(strip=True)
            result['original_price'] = self.parse_price(price_text)
        
        # Calculate discount
        if result['current_price'] and result['original_price']:
            result['is_on_sale'], result['discount_percent'] = self.calculate_discount(
                result['current_price'],
                result['original_price']
            )
        
        return result


class NordstromScraper(ProductScraper):
    """Scraper for Nordstrom products."""
    
    def scrape(self, url: str) -> Dict:
        """Scrape Nordstrom product page."""
        soup = self.fetch_page(url)
        
        if not soup:
            return {'error': 'Failed to fetch page'}
        
        result = {
            'name': None,
            'current_price': None,
            'original_price': None,
            'is_on_sale': False,
            'discount_percent': 0.0
        }
        
        # Product name
        name_elem = soup.select_one('h1[itemprop="name"]') or soup.select_one('h1.product-title')
        if name_elem:
            result['name'] = name_elem.get_text(strip=True)
        
        # Prices
        price_elem = soup.select_one('span[itemprop="price"]') or soup.select_one('.current-price')
        if price_elem:
            result['current_price'] = self.parse_price(price_elem.get('content') or price_elem.get_text())
        
        # Original price
        original_elem = soup.select_one('.original-price') or soup.select_one('s')
        if original_elem:
            result['original_price'] = self.parse_price(original_elem.get_text())
        
        # Calculate discount
        if result['current_price'] and result['original_price']:
            result['is_on_sale'], result['discount_percent'] = self.calculate_discount(
                result['current_price'],
                result['original_price']
            )
        
        return result


class GenericScraper(ProductScraper):
    """Generic scraper for other e-commerce sites."""
    
    def scrape(self, url: str) -> Dict:
        """Scrape generic product page using common patterns."""
        soup = self.fetch_page(url)
        
        if not soup:
            return {'error': 'Failed to fetch page'}
        
        result = {
            'name': None,
            'current_price': None,
            'original_price': None,
            'is_on_sale': False,
            'discount_percent': 0.0
        }
        
        # Try JSON-LD structured data first
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                import json
                data = json.loads(json_ld.string)
                if isinstance(data, list):
                    data = data[0]
                
                # Extract name
                if 'name' in data:
                    result['name'] = data['name']
                
                # Extract price
                if 'offers' in data:
                    offer = data['offers']
                    if isinstance(offer, list):
                        offer = offer[0]
                    
                    if 'price' in offer:
                        result['current_price'] = float(offer['price'])
                    
                    # Some sites include highPrice for original price
                    if 'highPrice' in offer:
                        result['original_price'] = float(offer['highPrice'])
            except Exception:
                pass
        
        # Fallback: Generic name selectors
        if not result['name']:
            name_selectors = [
                'h1[itemprop="name"]',
                'h1.product-title',
                'h1.product-name',
                'h1.product_title',
                'h1[data-product-title]',
                '.product-detail h1',
                'h1'
            ]
            
            for selector in name_selectors:
                name_elem = soup.select_one(selector)
                if name_elem:
                    result['name'] = name_elem.get_text(strip=True)
                    if len(result['name']) > 10:  # Sanity check
                        break
        
        # Generic price selectors
        if not result['current_price']:
            price_selectors = [
                'span[itemprop="price"]',
                '.price',
                '.product-price',
                '[data-product-price]',
                '.sale-price',
                '.current-price',
                '.price-now'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get('content') or price_elem.get_text(strip=True)
                    result['current_price'] = self.parse_price(price_text)
                    if result['current_price']:
                        break
        
        # Generic original price selectors
        if not result['original_price']:
            original_selectors = [
                '.original-price',
                '.regular-price',
                '.was-price',
                '.price-before-discount',
                'del .price',
                's .price',
                '.compare-at-price'
            ]
            
            for selector in original_selectors:
                orig_elem = soup.select_one(selector)
                if orig_elem:
                    price_text = orig_elem.get_text(strip=True)
                    result['original_price'] = self.parse_price(price_text)
                    if result['original_price']:
                        break
        
        # Calculate discount
        if result['current_price'] and result['original_price']:
            result['is_on_sale'], result['discount_percent'] = self.calculate_discount(
                result['current_price'],
                result['original_price']
            )
        
        return result


def scrape_product(url: str) -> Dict:
    """
    Main function to scrape a product URL.
    Routes to appropriate scraper based on domain.
    
    Args:
        url: Product URL
        
    Returns:
        Dictionary with product data or error
    """
    try:
        domain = urlparse(url).netloc.lower()
        
        # Route to appropriate scraper
        if 'etsy.com' in domain:
            scraper = EtsyScraper()
        elif 'nordstrom.com' in domain:
            scraper = NordstromScraper()
        elif any(indicator in domain for indicator in ['shopify', 'myshopify']):
            scraper = ShopifyScraper()
        else:
            # Try to detect Shopify by URL pattern or use generic
            scraper = GenericScraper()
            
            # Many sites use Shopify without obvious domain - try Shopify first
            result = ShopifyScraper().scrape(url)
            if result.get('name') and result.get('current_price'):
                return result
        
        # Scrape with selected scraper
        result = scraper.scrape(url)
        
        # Validate result has minimum required data
        if not result.get('error') and not result.get('name'):
            result['error'] = 'Could not extract product name'
        
        if not result.get('error') and not result.get('current_price'):
            result['error'] = 'Could not extract price'
        
        return result
        
    except Exception as e:
        return {'error': f'Scraping error: {str(e)}'}


if __name__ == '__main__':
    # Test scraper
    test_urls = [
        'https://melaniaclara.com/products/quinn-earrings-silver-clear',
        'https://www.etsy.com/listing/180164385/personalized-chinese-name-sterling',
    ]
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = scrape_product(url)
        print(result)

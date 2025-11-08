"""
Main price tracking orchestration script.
Coordinates scraping and database updates for all monitored products.
"""

import sys
import time
from datetime import datetime
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from database import (
    init_database,
    get_all_products,
    update_product_price,
    get_stats,
    get_new_sales
)
from scraper import scrape_product


def track_single_product(product: Dict) -> Dict:
    """
    Track a single product - scrape and update database.
    
    Args:
        product: Product dictionary from database
        
    Returns:
        Result dictionary with status
    """
    product_id = product['id']
    product_url = product['url']
    product_name = product['name']
    
    print(f"\n[{product_id}] Checking: {product_name}")
    print(f"    URL: {product_url}")
    
    # Scrape product
    result = scrape_product(product_url)
    
    # Check for errors
    if 'error' in result:
        print(f"    ❌ Error: {result['error']}")
        update_product_price(
            product_id=product_id,
            current_price=None,
            error=result['error']
        )
        return {
            'id': product_id,
            'name': product_name,
            'status': 'error',
            'error': result['error']
        }
    
    # Extract data
    current_price = result.get('current_price')
    original_price = result.get('original_price')
    is_on_sale = result.get('is_on_sale', False)
    discount_percent = result.get('discount_percent', 0)
    
    # Update database
    price_changed = update_product_price(
        product_id=product_id,
        current_price=current_price,
        original_price=original_price,
        is_on_sale=is_on_sale,
        discount_percent=discount_percent
    )
    
    # Report results
    if is_on_sale:
        print(f"    🔥 ON SALE: ${current_price:.2f} (was ${original_price:.2f}) - {discount_percent}% off")
    else:
        print(f"    💰 Price: ${current_price:.2f}")
    
    if price_changed:
        print(f"    📈 PRICE CHANGED!")
    
    return {
        'id': product_id,
        'name': product_name,
        'status': 'success',
        'current_price': current_price,
        'is_on_sale': is_on_sale,
        'discount_percent': discount_percent,
        'price_changed': price_changed
    }


def track_all_products(max_workers: int = 5) -> Dict:
    """
    Track all products in database with parallel execution.
    
    Args:
        max_workers: Maximum number of concurrent scrapers
        
    Returns:
        Summary dictionary
    """
    print("=" * 80)
    print("BLACK FRIDAY PRICE TRACKER")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get all products
    products = get_all_products()
    total_products = len(products)
    
    if total_products == 0:
        print("\n⚠️  No products in database. Run init_products.py first.")
        return {}
    
    print(f"\nTracking {total_products} products...\n")
    
    # Track results
    results = []
    successful = 0
    errors = 0
    price_changes = 0
    new_sales = 0
    
    # Use thread pool for parallel scraping (be respectful with rate)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_product = {
            executor.submit(track_single_product, product): product
            for product in products
        }
        
        # Process completed tasks
        for future in as_completed(future_to_product):
            product = future_to_product[future]
            try:
                result = future.result()
                results.append(result)
                
                if result['status'] == 'success':
                    successful += 1
                    if result.get('price_changed'):
                        price_changes += 1
                    if result.get('is_on_sale'):
                        new_sales += 1
                else:
                    errors += 1
                    
            except Exception as exc:
                print(f"\n❌ Exception tracking {product['name']}: {exc}")
                errors += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("TRACKING SUMMARY")
    print("=" * 80)
    print(f"Total Products: {total_products}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Errors: {errors}")
    print(f"📈 Price Changes: {price_changes}")
    print(f"🔥 On Sale: {new_sales}")
    
    # Get and display stats
    stats = get_stats()
    print("\n" + "=" * 80)
    print("CURRENT STATS")
    print("=" * 80)
    print(f"Products Tracked: {stats['total_products']}")
    print(f"On Sale: {stats['on_sale_count']} ({stats['on_sale_count']/stats['total_products']*100:.1f}%)")
    print(f"Not On Sale: {stats['not_on_sale_count']}")
    print(f"Average Discount: {stats['average_discount']}%")
    print(f"Total Potential Savings: ${stats['total_savings']:.2f}")
    print(f"Errors: {stats['error_count']}")
    
    # Show recent sales
    recent_sales = get_new_sales(hours=24)
    if recent_sales:
        print("\n" + "=" * 80)
        print("NEW SALES (Last 24 Hours)")
        print("=" * 80)
        for sale in recent_sales:
            print(f"\n🔥 {sale['name']}")
            print(f"   ${sale['current_price']:.2f} (was ${sale['original_price']:.2f})")
            print(f"   {sale['discount_percent']}% off")
            print(f"   {sale['url']}")
    
    print("\n" + "=" * 80)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return {
        'total': total_products,
        'successful': successful,
        'errors': errors,
        'price_changes': price_changes,
        'new_sales': new_sales,
        'stats': stats
    }


def main():
    """Main entry point."""
    # Initialize database if needed
    init_database()
    
    # Run tracker
    try:
        summary = track_all_products(max_workers=3)  # Conservative to avoid rate limits
        
        # Exit with appropriate code
        if summary.get('errors', 0) > 0:
            sys.exit(1)  # Some errors occurred
        else:
            sys.exit(0)  # All good
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Tracking interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

"""
Database module for Black Friday price tracking system.
Handles SQLite operations for products and price history.
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from contextlib import contextmanager

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'products.db')


@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """Initialize database with required tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Products table - stores current product information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                current_price REAL,
                original_price REAL,
                is_on_sale INTEGER DEFAULT 0,
                discount_percent REAL DEFAULT 0,
                currency TEXT DEFAULT 'USD',
                last_checked TIMESTAMP,
                last_price_change TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_count INTEGER DEFAULT 0,
                last_error TEXT
            )
        ''')
        
        # Price history table - tracks all price changes over time
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                price REAL NOT NULL,
                original_price REAL,
                is_on_sale INTEGER DEFAULT 0,
                discount_percent REAL DEFAULT 0,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_products_url ON products(url)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_price_history_product_id 
            ON price_history(product_id, checked_at DESC)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_products_on_sale 
            ON products(is_on_sale, discount_percent DESC)
        ''')
        
        conn.commit()
        print(f"Database initialized at {DB_PATH}")


def add_product(url: str, name: str) -> int:
    """
    Add a new product to the database.
    
    Args:
        url: Product URL
        name: Product name
        
    Returns:
        Product ID
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (url, name, created_at)
            VALUES (?, ?, ?)
        ''', (url, name, datetime.now()))
        return cursor.lastrowid


def update_product_price(
    product_id: int,
    current_price: Optional[float],
    original_price: Optional[float] = None,
    is_on_sale: bool = False,
    discount_percent: float = 0,
    error: Optional[str] = None
) -> bool:
    """
    Update product price information.
    
    Args:
        product_id: Product ID
        current_price: Current price (None if scraping failed)
        original_price: Original price before discount
        is_on_sale: Whether product is on sale
        discount_percent: Discount percentage
        error: Error message if scraping failed
        
    Returns:
        True if price changed, False otherwise
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get current product data
        cursor.execute('SELECT current_price FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        
        if not row:
            return False
            
        old_price = row['current_price']
        price_changed = old_price != current_price and current_price is not None
        
        # Update product record
        now = datetime.now()
        
        if error:
            # Handle scraping error
            cursor.execute('''
                UPDATE products 
                SET last_checked = ?,
                    error_count = error_count + 1,
                    last_error = ?
                WHERE id = ?
            ''', (now, error, product_id))
        else:
            # Successful scrape
            cursor.execute('''
                UPDATE products 
                SET current_price = ?,
                    original_price = ?,
                    is_on_sale = ?,
                    discount_percent = ?,
                    last_checked = ?,
                    last_price_change = CASE WHEN ? THEN ? ELSE last_price_change END,
                    error_count = 0,
                    last_error = NULL
                WHERE id = ?
            ''', (
                current_price,
                original_price,
                1 if is_on_sale else 0,
                discount_percent,
                now,
                price_changed,
                now,
                product_id
            ))
            
            # Add to price history
            cursor.execute('''
                INSERT INTO price_history 
                (product_id, price, original_price, is_on_sale, discount_percent, checked_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                product_id,
                current_price,
                original_price,
                1 if is_on_sale else 0,
                discount_percent,
                now
            ))
        
        return price_changed


def get_all_products() -> List[Dict]:
    """
    Get all products with current information.
    
    Returns:
        List of product dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id,
                url,
                name,
                current_price,
                original_price,
                is_on_sale,
                discount_percent,
                currency,
                last_checked,
                last_price_change,
                created_at,
                error_count,
                last_error
            FROM products
            ORDER BY name
        ''')
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row['id'],
                'url': row['url'],
                'name': row['name'],
                'current_price': row['current_price'],
                'original_price': row['original_price'],
                'is_on_sale': bool(row['is_on_sale']),
                'discount_percent': row['discount_percent'],
                'currency': row['currency'],
                'last_checked': row['last_checked'],
                'last_price_change': row['last_price_change'],
                'created_at': row['created_at'],
                'error_count': row['error_count'],
                'last_error': row['last_error']
            })
        
        return products


def get_product_by_url(url: str) -> Optional[Dict]:
    """
    Get product by URL.
    
    Args:
        url: Product URL
        
    Returns:
        Product dictionary or None
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id, url, name, current_price, original_price,
                is_on_sale, discount_percent, currency,
                last_checked, last_price_change, created_at
            FROM products
            WHERE url = ?
        ''', (url,))
        
        row = cursor.fetchone()
        if not row:
            return None
            
        return {
            'id': row['id'],
            'url': row['url'],
            'name': row['name'],
            'current_price': row['current_price'],
            'original_price': row['original_price'],
            'is_on_sale': bool(row['is_on_sale']),
            'discount_percent': row['discount_percent'],
            'currency': row['currency'],
            'last_checked': row['last_checked'],
            'last_price_change': row['last_price_change'],
            'created_at': row['created_at']
        }


def get_price_history(product_id: int, limit: int = 100) -> List[Dict]:
    """
    Get price history for a product.
    
    Args:
        product_id: Product ID
        limit: Maximum number of records to return
        
    Returns:
        List of price history records
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                price,
                original_price,
                is_on_sale,
                discount_percent,
                checked_at
            FROM price_history
            WHERE product_id = ?
            ORDER BY checked_at DESC
            LIMIT ?
        ''', (product_id, limit))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'price': row['price'],
                'original_price': row['original_price'],
                'is_on_sale': bool(row['is_on_sale']),
                'discount_percent': row['discount_percent'],
                'checked_at': row['checked_at']
            })
        
        return history


def get_stats() -> Dict:
    """
    Get summary statistics about tracked products.
    
    Returns:
        Dictionary with stats
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Total products
        cursor.execute('SELECT COUNT(*) as count FROM products')
        total_products = cursor.fetchone()['count']
        
        # Products on sale
        cursor.execute('SELECT COUNT(*) as count FROM products WHERE is_on_sale = 1')
        on_sale_count = cursor.fetchone()['count']
        
        # Average discount
        cursor.execute('''
            SELECT AVG(discount_percent) as avg_discount 
            FROM products 
            WHERE is_on_sale = 1 AND discount_percent > 0
        ''')
        avg_discount = cursor.fetchone()['avg_discount'] or 0
        
        # Total potential savings (sum of discounts)
        cursor.execute('''
            SELECT SUM(original_price - current_price) as total_savings
            FROM products
            WHERE is_on_sale = 1 
            AND original_price IS NOT NULL 
            AND current_price IS NOT NULL
        ''')
        total_savings = cursor.fetchone()['total_savings'] or 0
        
        # Products with errors
        cursor.execute('SELECT COUNT(*) as count FROM products WHERE error_count > 0')
        error_count = cursor.fetchone()['count']
        
        # Last check time
        cursor.execute('SELECT MAX(last_checked) as last_check FROM products')
        last_check = cursor.fetchone()['last_check']
        
        return {
            'total_products': total_products,
            'on_sale_count': on_sale_count,
            'not_on_sale_count': total_products - on_sale_count,
            'average_discount': round(avg_discount, 2),
            'total_savings': round(total_savings, 2),
            'error_count': error_count,
            'last_check': last_check
        }


def get_new_sales(hours: int = 24) -> List[Dict]:
    """
    Get products that went on sale recently.
    
    Args:
        hours: Number of hours to look back
        
    Returns:
        List of products with new sales
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id, url, name, current_price, original_price,
                discount_percent, last_price_change
            FROM products
            WHERE is_on_sale = 1
            AND last_price_change >= datetime('now', '-' || ? || ' hours')
            ORDER BY discount_percent DESC
        ''', (hours,))
        
        sales = []
        for row in cursor.fetchall():
            sales.append({
                'id': row['id'],
                'url': row['url'],
                'name': row['name'],
                'current_price': row['current_price'],
                'original_price': row['original_price'],
                'discount_percent': row['discount_percent'],
                'last_price_change': row['last_price_change']
            })
        
        return sales


if __name__ == '__main__':
    # Initialize database when run directly
    init_database()
    print("Database setup complete!")

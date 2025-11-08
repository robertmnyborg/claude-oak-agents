"""
Flask API for Black Friday price tracking dashboard.
Serves product data and statistics via REST API.
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

from database import (
    init_database,
    get_all_products,
    get_price_history,
    get_stats,
    get_new_sales
)

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for development

# Initialize database on startup
init_database()


@app.route('/')
def index():
    """Serve dashboard HTML."""
    return send_from_directory('static', 'dashboard.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Get all products with current status.
    
    Returns:
        JSON array of products
    """
    try:
        products = get_all_products()
        
        # Format for frontend
        formatted_products = []
        for product in products:
            formatted_products.append({
                'id': product['id'],
                'name': product['name'],
                'url': product['url'],
                'currentPrice': product['current_price'],
                'originalPrice': product['original_price'],
                'isOnSale': product['is_on_sale'],
                'discountPercent': product['discount_percent'],
                'currency': product['currency'],
                'lastChecked': product['last_checked'],
                'lastPriceChange': product['last_price_change'],
                'errorCount': product['error_count'],
                'lastError': product['last_error']
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted_products),
            'products': formatted_products
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/products/<int:product_id>/history', methods=['GET'])
def get_product_history(product_id):
    """
    Get price history for a specific product.
    
    Args:
        product_id: Product ID
        
    Returns:
        JSON array of price history
    """
    try:
        history = get_price_history(product_id, limit=100)
        
        # Format for frontend
        formatted_history = []
        for record in history:
            formatted_history.append({
                'price': record['price'],
                'originalPrice': record['original_price'],
                'isOnSale': record['is_on_sale'],
                'discountPercent': record['discount_percent'],
                'checkedAt': record['checked_at']
            })
        
        return jsonify({
            'success': True,
            'productId': product_id,
            'count': len(formatted_history),
            'history': formatted_history
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    Get summary statistics.
    
    Returns:
        JSON object with stats
    """
    try:
        stats = get_stats()
        
        return jsonify({
            'success': True,
            'stats': {
                'totalProducts': stats['total_products'],
                'onSaleCount': stats['on_sale_count'],
                'notOnSaleCount': stats['not_on_sale_count'],
                'averageDiscount': stats['average_discount'],
                'totalSavings': stats['total_savings'],
                'errorCount': stats['error_count'],
                'lastCheck': stats['last_check']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sales/recent', methods=['GET'])
def get_recent_sales():
    """
    Get products that recently went on sale.
    
    Returns:
        JSON array of recent sales
    """
    try:
        sales = get_new_sales(hours=24)
        
        # Format for frontend
        formatted_sales = []
        for sale in sales:
            formatted_sales.append({
                'id': sale['id'],
                'name': sale['name'],
                'url': sale['url'],
                'currentPrice': sale['current_price'],
                'originalPrice': sale['original_price'],
                'discountPercent': sale['discount_percent'],
                'lastPriceChange': sale['last_price_change']
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted_sales),
            'sales': formatted_sales
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/products/on-sale', methods=['GET'])
def get_on_sale_products():
    """
    Get all products currently on sale, sorted by discount.
    
    Returns:
        JSON array of products on sale
    """
    try:
        all_products = get_all_products()
        
        # Filter and sort by discount
        on_sale = [
            p for p in all_products
            if p['is_on_sale'] and p['discount_percent'] > 0
        ]
        on_sale.sort(key=lambda x: x['discount_percent'], reverse=True)
        
        # Format for frontend
        formatted_products = []
        for product in on_sale:
            formatted_products.append({
                'id': product['id'],
                'name': product['name'],
                'url': product['url'],
                'currentPrice': product['current_price'],
                'originalPrice': product['original_price'],
                'discountPercent': product['discount_percent'],
                'savings': product['original_price'] - product['current_price'],
                'lastChecked': product['last_checked']
            })
        
        return jsonify({
            'success': True,
            'count': len(formatted_products),
            'products': formatted_products
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run Flask development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"\n🚀 Black Friday Tracker API starting on port {port}")
    print(f"   Dashboard: http://localhost:{port}/")
    print(f"   API Docs: http://localhost:{port}/api/health")
    print(f"   Debug mode: {debug}\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

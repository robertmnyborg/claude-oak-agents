# Black Friday Sale Tracker

A comprehensive Python-based system for monitoring 70 product URLs across multiple e-commerce platforms to detect sales, price changes, and discounts. Perfect for Black Friday and Cyber Monday deal hunting.

## Features

- **Multi-Platform Support**: Works with Shopify, Etsy, Nordstrom, Amazon, Target, and more
- **Smart Price Detection**: Extracts current price, original price, and calculates discounts
- **Price History Tracking**: SQLite database stores all price changes over time
- **Sale Alerts**: Automatically detects when products go on sale
- **Web Dashboard**: Beautiful Flask-based dashboard to view all products and deals
- **REST API**: Complete API for custom integrations
- **Automated Scheduling**: Cron job support for daily price checks
- **Graceful Error Handling**: Handles rate limiting and scraping failures

## Project Structure

```
cj-black-friday-alerts/
├── database.py          # SQLite database operations
├── scraper.py           # Web scraping logic (multi-platform)
├── tracker.py           # Main tracking orchestration
├── app.py               # Flask API and dashboard backend
├── init_products.py     # Initialize database with 70 URLs
├── scheduler.sh         # Cron job script for daily checks
├── requirements.txt     # Python dependencies
├── static/
│   └── dashboard.html   # Web dashboard frontend
└── data/
    └── products.db      # SQLite database (auto-created)
```

## Installation

### 1. Clone or Download

```bash
cd cj-black-friday-alerts
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Initialize Database with Product URLs

```bash
python init_products.py
```

This will:
- Create SQLite database at `data/products.db`
- Add all 70 product URLs
- Set up necessary tables and indexes

**Output:**
```
Initializing Black Friday Price Tracker Database
================================================================================
✅ Added [1]: Melania Clara - Quinn Earrings
✅ Added [2]: Etsy - Chinese Name Necklace
...
================================================================================
INITIALIZATION COMPLETE
================================================================================
Products Added: 70
Total Products: 70
```

### 2. Run Initial Price Check

```bash
python tracker.py
```

This will:
- Scrape all 70 product URLs
- Extract current prices and sale information
- Store data in database
- Display summary report

**Output:**
```
================================================================================
BLACK FRIDAY PRICE TRACKER
Started: 2024-11-09 14:30:00
================================================================================
Tracking 70 products...

[1] Checking: Melania Clara - Quinn Earrings
    URL: https://melaniaclara.com/products/quinn-earrings-silver-clear
    💰 Price: $45.00

[2] Checking: Etsy - Chinese Name Necklace
    🔥 ON SALE: $32.99 (was $45.99) - 28% off
    📈 PRICE CHANGED!

...

================================================================================
TRACKING SUMMARY
================================================================================
Total Products: 70
✅ Successful: 68
❌ Errors: 2
📈 Price Changes: 5
🔥 On Sale: 12

================================================================================
CURRENT STATS
================================================================================
Products Tracked: 70
On Sale: 12 (17.1%)
Average Discount: 23.5%
Total Potential Savings: $456.78
```

### 3. Start Web Dashboard

```bash
python app.py
```

**Access dashboard at:** http://localhost:5000

The dashboard shows:
- Summary statistics (total products, on sale count, average discount, savings)
- Product grid with filters (All / On Sale / Regular Price)
- Real-time price information
- Links to product pages

### 4. Set Up Daily Automated Checks (Optional)

```bash
# Make scheduler executable
chmod +x scheduler.sh

# Edit crontab
crontab -e

# Add line for daily 8am PST check (adjust timezone as needed)
0 8 * * * /path/to/cj-black-friday-alerts/scheduler.sh
```

**Timezone Conversion for 8am PST:**
- PST (server in Pacific): `0 8 * * *`
- EST (server in Eastern): `0 11 * * *`
- UTC (server in UTC): `0 16 * * *`

Logs will be saved to `logs/tracker-YYYY-MM-DD.log`

## API Reference

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-09T14:30:00Z"
}
```

#### GET /api/products
Get all products with current status.

**Response:**
```json
{
  "success": true,
  "count": 70,
  "products": [
    {
      "id": 1,
      "name": "Melania Clara - Quinn Earrings",
      "url": "https://...",
      "currentPrice": 45.00,
      "originalPrice": null,
      "isOnSale": false,
      "discountPercent": 0,
      "lastChecked": "2024-11-09T14:30:00",
      "errorCount": 0
    },
    ...
  ]
}
```

#### GET /api/products/:id/history
Get price history for a specific product.

**Response:**
```json
{
  "success": true,
  "productId": 1,
  "count": 5,
  "history": [
    {
      "price": 45.00,
      "originalPrice": null,
      "isOnSale": false,
      "discountPercent": 0,
      "checkedAt": "2024-11-09T14:30:00"
    },
    ...
  ]
}
```

#### GET /api/stats
Get summary statistics.

**Response:**
```json
{
  "success": true,
  "stats": {
    "totalProducts": 70,
    "onSaleCount": 12,
    "notOnSaleCount": 58,
    "averageDiscount": 23.5,
    "totalSavings": 456.78,
    "errorCount": 2,
    "lastCheck": "2024-11-09T14:30:00"
  }
}
```

#### GET /api/sales/recent
Get products that went on sale in the last 24 hours.

**Response:**
```json
{
  "success": true,
  "count": 3,
  "sales": [
    {
      "id": 2,
      "name": "Etsy - Chinese Name Necklace",
      "url": "https://...",
      "currentPrice": 32.99,
      "originalPrice": 45.99,
      "discountPercent": 28.3,
      "lastPriceChange": "2024-11-09T08:15:00"
    },
    ...
  ]
}
```

#### GET /api/products/on-sale
Get all products currently on sale, sorted by discount percentage.

**Response:**
```json
{
  "success": true,
  "count": 12,
  "products": [
    {
      "id": 5,
      "name": "Quince - Mongolian Cashmere Crewneck",
      "url": "https://...",
      "currentPrice": 39.99,
      "originalPrice": 79.99,
      "discountPercent": 50.0,
      "savings": 40.00,
      "lastChecked": "2024-11-09T14:30:00"
    },
    ...
  ]
}
```

## Database Schema

### products table
- `id` - Primary key
- `url` - Product URL (unique)
- `name` - Product name
- `current_price` - Current price
- `original_price` - Original/compare-at price
- `is_on_sale` - Boolean sale status
- `discount_percent` - Discount percentage
- `currency` - Currency (default: USD)
- `last_checked` - Last check timestamp
- `last_price_change` - Last price change timestamp
- `created_at` - Product added timestamp
- `error_count` - Number of scraping errors
- `last_error` - Last error message

### price_history table
- `id` - Primary key
- `product_id` - Foreign key to products
- `price` - Recorded price
- `original_price` - Recorded original price
- `is_on_sale` - Sale status at time
- `discount_percent` - Discount at time
- `checked_at` - Timestamp

## Scraper Architecture

### Supported Platforms

The scraper includes specialized extractors for:

- **Shopify** - Detects Shopify stores, uses JSON-LD structured data
- **Etsy** - Custom selectors for Etsy product pages
- **Nordstrom** - Schema.org microdata extraction
- **Generic** - Fallback for other e-commerce platforms

### Price Detection Strategy

1. **JSON-LD Structured Data** (most reliable)
2. **HTML Meta Tags** (Open Graph, Schema.org)
3. **CSS Selectors** (platform-specific patterns)
4. **Text Parsing** (fallback)

### Sale Detection

Sales are detected by comparing:
- Current price vs original price
- Presence of compare-at price elements
- Discount badges and sale indicators

### Rate Limiting

- Random delays between requests (0.5-2 seconds)
- User agent rotation
- Respectful scraping (3 concurrent workers by default)

### Error Handling

- Network errors logged and retried
- Scraping failures stored in database
- Error count tracking per product
- Graceful degradation (continue with other products)

## Customization

### Adding New Products

Edit `init_products.py` and add to the `PRODUCTS` list:

```python
PRODUCTS = [
    {
        "name": "Your Product Name",
        "url": "https://example.com/product-url"
    },
    ...
]
```

Then run:
```bash
python init_products.py
```

### Adjusting Scraper Workers

In `tracker.py`, adjust `max_workers`:

```python
track_all_products(max_workers=3)  # Default: 3 (conservative)
# Increase for faster scraping (but higher rate limit risk)
# track_all_products(max_workers=10)
```

### Custom Platform Scrapers

To add a new platform scraper, edit `scraper.py`:

```python
class CustomPlatformScraper(ProductScraper):
    """Scraper for custom platform."""
    
    def scrape(self, url: str) -> Dict:
        soup = self.fetch_page(url)
        # ... custom extraction logic
        return result
```

Then update `scrape_product()` routing:

```python
def scrape_product(url: str) -> Dict:
    domain = urlparse(url).netloc.lower()
    
    if 'customplatform.com' in domain:
        scraper = CustomPlatformScraper()
    # ...
```

## Deployment

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

```bash
export PORT=5000          # Server port (default: 5000)
export DEBUG=False        # Debug mode (default: True)
```

### Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t black-friday-tracker .
docker run -p 5000:5000 -v $(pwd)/data:/app/data black-friday-tracker
```

## Troubleshooting

### Problem: Scraper returns errors for all products

**Solution:** Some sites block automated requests. Try:
1. Reduce `max_workers` in `tracker.py`
2. Increase delays in `scraper.py`
3. Check if site requires JavaScript (consider using Selenium)

### Problem: Database locked errors

**Solution:** SQLite doesn't handle high concurrency well:
1. Reduce `max_workers`
2. Or migrate to PostgreSQL for production

### Problem: Prices not detected

**Solution:** Site's HTML structure may have changed:
1. Check `last_error` in database
2. Manually inspect product page HTML
3. Update CSS selectors in `scraper.py`

### Problem: Cron job not running

**Solution:**
1. Check cron logs: `grep CRON /var/log/syslog`
2. Ensure script has execute permissions: `chmod +x scheduler.sh`
3. Use absolute paths in crontab
4. Check timezone settings

## Performance

- **Scraping Speed**: ~20-30 products/minute (3 workers)
- **Database Size**: ~1MB per 1000 price records
- **Memory Usage**: ~50-100MB during scraping
- **API Response Time**: <100ms for most endpoints

## License

MIT License - Use for personal or commercial projects.

## Credits

Built with:
- **Python 3.8+**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Flask** - Web framework
- **SQLite** - Database

## Support

For issues or questions:
1. Check this README
2. Review error logs in `logs/`
3. Inspect database with `sqlite3 data/products.db`
4. Check product URLs are still valid

## Future Enhancements

Potential improvements:
- Email/SMS notifications for new sales
- Price drop alerts (threshold-based)
- Historical price charts
- Export to CSV/Excel
- Mobile app
- Telegram bot integration
- Browser extension

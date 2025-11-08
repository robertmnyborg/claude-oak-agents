# Dashboard Quick Start Guide

Get the Black Friday Sale Tracker dashboard running in 3 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

### 1. Install Dependencies (30 seconds)

```bash
cd cj-black-friday-alerts
pip install -r requirements.txt
```

### 2. Initialize Database (30 seconds)

```bash
python init_products.py
```

This creates the database and loads 70 sample products.

### 3. Start the Server (5 seconds)

```bash
python app.py
```

You should see:
```
🚀 Black Friday Tracker API starting on port 5000
   Dashboard: http://localhost:5000/
   API Docs: http://localhost:5000/api/health
   Debug mode: True
```

### 4. Open Dashboard

Open your browser to:
```
http://localhost:5000/
```

You should see the dashboard with:
- 4 statistics cards at the top
- Filter tabs (All Products / On Sale Only / Regular Price)
- Sort dropdown
- Product grid with cards
- Auto-refresh countdown timer

## What You'll See

### Statistics Cards
1. **Total Products**: 70 (or however many you loaded)
2. **Items On Sale**: Count of products with discounts
3. **Average Discount**: Average percentage off
4. **Total Savings**: Sum of all potential savings

### Product Cards
Each card shows:
- Product name and retailer
- Current price (large, green)
- Original price (strikethrough if on sale)
- Red "SALE X% OFF" badge (if on sale)
- Savings amount
- "View Product" button
- Last checked timestamp

### Filtering
- **All Products**: Shows everything (default)
- **On Sale Only**: Shows only discounted items
- **Regular Price**: Shows only non-discounted items

### Sorting
- **Discount % (High to Low)**: Best deals first (default)
- **Discount % (Low to High)**: Smallest discounts first
- **Price (Low to High)**: Cheapest items first
- **Price (High to Low)**: Most expensive items first
- **Recently Checked**: Most recently updated first

### Auto-Refresh
- Dashboard refreshes every 5 minutes automatically
- Countdown timer shows time until next refresh
- Click "Refresh Now" button to update immediately
- Spinning icon shows when loading

## Testing Features

### 1. Test Filtering
1. Click "On Sale Only" tab
2. Only products with discounts should show
3. Click "Regular Price" tab
4. Only products without discounts should show
5. Click "All Products" to see everything

### 2. Test Sorting
1. Select "Price (Low to High)" from dropdown
2. Products should reorder by price (cheapest first)
3. Select "Discount % (High to Low)"
4. Products with highest discounts should appear first

### 3. Test Auto-Refresh
1. Watch the countdown timer
2. After 5 minutes, data will refresh automatically
3. Or click "Refresh Now" to trigger immediately
4. Watch the spinning icon during refresh

### 4. Test Persistence
1. Select "On Sale Only" and "Price (Low to High)"
2. Refresh the page (F5)
3. Your filter and sort should be remembered

### 5. Test Responsive Design
1. Resize browser window
2. On desktop: 3-4 cards per row
3. On tablet: 2-3 cards per row
4. On mobile: 1 card per row

### 6. Test Product Links
1. Click "View Product" button on any card
2. Product URL should open in new tab
3. Or click anywhere on the card to open product

## Customization

### Change Refresh Interval

Edit `static/dashboard.html` (line 698):
```javascript
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes
// Change to 2 minutes:
const REFRESH_INTERVAL = 2 * 60 * 1000;
```

### Change Colors

Edit `static/dashboard.html` (lines 9-18):
```css
:root {
    --primary: #DC2626;      /* Red - change to #0000FF for blue */
    --secondary: #1F2937;    /* Dark gray */
    --accent: #F59E0B;       /* Gold */
    --background: #F9FAFB;   /* Light gray */
    --on-sale-bg: #FEE2E2;   /* Light red */
    --success: #10B981;      /* Green */
}
```

### Change Card Size

Edit `static/dashboard.html` (line 304):
```css
.products-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    /* Change 300px to 400px for larger cards */
    /* Change 300px to 250px for smaller cards */
}
```

## Running with Real Data

### 1. Set Up Web Scraping

The system includes scrapers for:
- Melania Clara (jewelry)
- Missguided (fashion)
- Everlane (apparel)
- Tarte Cosmetics (makeup)

To enable automatic price checking:

```bash
# Edit scheduler.sh to enable scraping
nano scheduler.sh

# Run scraper manually
python scraper.py
```

### 2. Schedule Automatic Updates

On Linux/Mac (cron):
```bash
# Edit crontab
crontab -e

# Add line to run every hour
0 * * * * cd /path/to/cj-black-friday-alerts && ./scheduler.sh
```

On Windows (Task Scheduler):
- Create task to run `scheduler.sh` every hour

## Troubleshooting

### Dashboard Shows "Error Loading Data"

**Check server is running:**
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2025-11-09T..."}
```

If no response, restart server:
```bash
python app.py
```

### No Products Showing

**Check database:**
```bash
sqlite3 data/products.db "SELECT COUNT(*) FROM products;"
```

Should show 70 (or number of products you loaded).

If 0, reinitialize:
```bash
python init_products.py
```

### Styles Look Broken

**Clear browser cache:**
- Chrome/Edge: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Firefox: Ctrl+F5 (Cmd+Shift+R on Mac)
- Safari: Cmd+Option+R

### Port 5000 Already in Use

**Change port:**
```bash
PORT=8000 python app.py
```

Then open `http://localhost:8000/`

### Python Module Errors

**Reinstall dependencies:**
```bash
pip install --force-reinstall -r requirements.txt
```

## Next Steps

1. **Add Real Products**: Edit `init_products.py` to add your tracked products
2. **Enable Scraping**: Configure scrapers for automatic price updates
3. **Deploy to Production**: See `DEPLOYMENT.md` for hosting options
4. **Customize Design**: Edit `static/dashboard.html` to match your brand
5. **Add Features**: See `static/DASHBOARD_README.md` for enhancement ideas

## API Endpoints

For developers who want to integrate with the API:

```bash
# Health check
curl http://localhost:5000/api/health

# Get statistics
curl http://localhost:5000/api/stats

# Get all products
curl http://localhost:5000/api/products

# Get product price history
curl http://localhost:5000/api/products/1/history

# Get recent sales (24 hours)
curl http://localhost:5000/api/sales/recent

# Get products on sale
curl http://localhost:5000/api/products/on-sale
```

## File Structure

```
cj-black-friday-alerts/
├── static/
│   ├── dashboard.html          # Main dashboard (THIS FILE)
│   ├── DASHBOARD_README.md     # Detailed documentation
│   └── DASHBOARD_QUICKSTART.md # This file
├── app.py                      # Flask server
├── database.py                 # Database operations
├── init_products.py            # Initialize sample data
├── scraper.py                  # Web scraping
├── requirements.txt            # Python dependencies
└── data/
    └── products.db            # SQLite database
```

## Getting Help

- **Dashboard Documentation**: See `static/DASHBOARD_README.md`
- **Project README**: See main `README.md`
- **API Documentation**: See `app.py` docstrings
- **Database Schema**: See `database.py`

## Summary

You now have a fully functional Black Friday sale tracking dashboard!

**Key Points:**
- Dashboard auto-refreshes every 5 minutes
- Filter by sale status
- Sort by price or discount
- Click cards to view products
- Mobile-responsive design
- No build tools needed (single HTML file)

**Enjoy tracking those Black Friday deals!** 🔥

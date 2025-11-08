# Quick Start Guide

Get your Black Friday tracker running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

## Installation (3 minutes)

```bash
# 1. Navigate to project directory
cd cj-black-friday-alerts

# 2. Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## First Run (2 minutes)

```bash
# 1. Initialize database with 70 product URLs
python init_products.py

# Expected output:
# ✅ Added [1]: Melania Clara - Quinn Earrings
# ✅ Added [2]: Etsy - Chinese Name Necklace
# ...
# Products Added: 70

# 2. Run first price check (takes 3-5 minutes)
python tracker.py

# Expected output:
# Tracking 70 products...
# [1] Checking: Melania Clara - Quinn Earrings
#     💰 Price: $45.00
# ...
# Total Products: 70
# ✅ Successful: 68
# 🔥 On Sale: 12

# 3. Start web dashboard
python app.py

# Expected output:
# 🚀 Black Friday Tracker API starting on port 5000
# Dashboard: http://localhost:5000/
```

## View Dashboard

Open your browser to: **http://localhost:5000**

You'll see:
- Summary stats (total products, sales, savings)
- Product grid with filters
- Real-time sale information

## Set Up Daily Checks (Optional)

```bash
# Edit cron jobs
crontab -e

# Add this line for daily 8am checks:
0 8 * * * /full/path/to/cj-black-friday-alerts/scheduler.sh
```

Replace `/full/path/to/` with your actual directory path.

## Test Scraper (Optional)

```bash
# Test scraper on a few sample URLs
python test_scraper.py

# Expected output:
# Testing: Shopify Store
# ✅ Name: Quinn Earrings
# 💰 Current Price: $45.00
```

## Troubleshooting

**ImportError: No module named 'requests'**
- Make sure you activated virtual environment: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

**No products in database**
- Run initialization: `python init_products.py`

**Port 5000 already in use**
- Use different port: `PORT=8000 python app.py`
- Or stop other service using port 5000

**Scraping errors**
- Normal to have 2-5% error rate (rate limiting, timeouts)
- Check logs in `logs/` directory
- Reduce workers if too many errors: edit `tracker.py`, set `max_workers=1`

## Next Steps

1. **Monitor Dashboard**: Keep dashboard open during Black Friday
2. **Check Logs**: Review `logs/tracker-*.log` for detailed results
3. **Customize URLs**: Edit `init_products.py` to add your products
4. **Set Alerts**: Modify `scheduler.sh` to send email notifications

## File Overview

- `database.py` - Database operations
- `scraper.py` - Web scraping logic
- `tracker.py` - Main tracking script
- `app.py` - Web dashboard server
- `init_products.py` - Product initialization
- `scheduler.sh` - Cron job script

## API Endpoints

Base URL: `http://localhost:5000/api`

- `GET /api/products` - All products
- `GET /api/products/on-sale` - Products on sale
- `GET /api/stats` - Summary statistics
- `GET /api/sales/recent` - Sales in last 24 hours

## Support

See full documentation in `README.md`

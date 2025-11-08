# Black Friday Sale Tracker - Documentation Index

Quick navigation to all project documentation and resources.

## 🚀 Getting Started

**New to this project? Start here:**

1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - High-level overview (5 min read)
2. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
3. **[README.md](README.md)** - Complete user manual

## 📚 Documentation by Role

### For End Users
- **[QUICKSTART.md](QUICKSTART.md)** - Fastest way to get started
- **[README.md](README.md)** - Complete guide with examples
- **Dashboard:** http://localhost:5000 (after running `python app.py`)

### For Developers
- **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** - Architecture and technical details
- **[README.md](README.md)** - API reference and customization
- **[database.py](database.py)** - Database schema and operations
- **[scraper.py](scraper.py)** - Scraping logic and platform support
- **[tracker.py](tracker.py)** - Orchestration workflow
- **[app.py](app.py)** - Flask API endpoints

### For DevOps / System Admins
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[scheduler.sh](scheduler.sh)** - Cron job automation
- **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** - Performance and monitoring

## 📋 Documentation by Topic

### Setup & Installation
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [README.md](README.md) - Installation section
- [requirements.txt](requirements.txt) - Python dependencies

### Configuration
- [init_products.py](init_products.py) - Product URL configuration
- [scheduler.sh](scheduler.sh) - Cron job configuration
- [app.py](app.py) - API server configuration

### Usage
- [README.md](README.md) - Complete usage guide
- [QUICKSTART.md](QUICKSTART.md) - Quick usage examples
- [static/dashboard.html](static/dashboard.html) - Web UI

### API Reference
- [README.md](README.md) - API endpoints section
- [app.py](app.py) - Implementation details
- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) - API architecture

### Deployment
- [DEPLOYMENT.md](DEPLOYMENT.md) - All deployment options
- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) - Production considerations
- [README.md](README.md) - Deployment section

### Development
- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) - Architecture overview
- [database.py](database.py) - Database layer
- [scraper.py](scraper.py) - Scraping engine
- [tracker.py](tracker.py) - Orchestration
- [app.py](app.py) - API server
- [test_scraper.py](test_scraper.py) - Testing utilities

### Troubleshooting
- [README.md](README.md) - Troubleshooting section
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production issues
- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) - Common problems

## 🔍 Quick Reference

### Commands

```bash
# Setup
pip install -r requirements.txt
python init_products.py

# Daily Usage
python tracker.py        # Run price check
python app.py            # Start dashboard

# Testing
python test_scraper.py   # Test scraper

# Automation
chmod +x scheduler.sh
crontab -e              # Add cron job
```

### File Purpose

| File | Purpose | When to Use |
|------|---------|-------------|
| `database.py` | Database operations | Modify schema, add queries |
| `scraper.py` | Web scraping | Add platforms, fix selectors |
| `tracker.py` | Main orchestration | Adjust workers, logging |
| `app.py` | Flask API | Add endpoints, modify API |
| `init_products.py` | Product initialization | Add/remove products |
| `scheduler.sh` | Cron automation | Configure schedule |
| `test_scraper.py` | Testing | Verify scraping works |

### URLs

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:5000 |
| API Health | http://localhost:5000/api/health |
| All Products | http://localhost:5000/api/products |
| Statistics | http://localhost:5000/api/stats |
| On Sale | http://localhost:5000/api/products/on-sale |

## 📖 Reading Order Recommendations

### First Time Setup
1. PROJECT_SUMMARY.md (overview)
2. QUICKSTART.md (installation)
3. README.md (usage examples)
4. Test run with `python tracker.py`
5. Explore dashboard at http://localhost:5000

### Production Deployment
1. README.md (understand features)
2. DEPLOYMENT.md (deployment options)
3. SYSTEM_OVERVIEW.md (architecture)
4. Choose deployment method
5. Follow deployment guide

### Custom Development
1. SYSTEM_OVERVIEW.md (architecture)
2. Code files (database.py, scraper.py, etc.)
3. README.md (API reference)
4. Make changes
5. Test with test_scraper.py

### Troubleshooting
1. Check logs in `logs/` directory
2. Review README.md troubleshooting section
3. Check SYSTEM_OVERVIEW.md for technical details
4. Run test_scraper.py to isolate issues
5. Review DEPLOYMENT.md for production issues

## 🎯 Common Tasks

### Task: Add New Products
**Files:** `init_products.py`
**Steps:**
1. Edit `PRODUCTS` list in init_products.py
2. Run `python init_products.py`
3. Run `python tracker.py` to check prices

### Task: Change Schedule
**Files:** `scheduler.sh`, crontab
**Steps:**
1. Run `crontab -e`
2. Modify schedule time
3. Save and exit

### Task: Add New Platform Scraper
**Files:** `scraper.py`
**Steps:**
1. Create new scraper class in scraper.py
2. Add routing in `scrape_product()`
3. Test with test_scraper.py

### Task: Deploy to Production
**Files:** DEPLOYMENT.md
**Steps:**
1. Choose deployment method from DEPLOYMENT.md
2. Follow relevant section
3. Configure systemd/Docker
4. Set up monitoring

### Task: View Price History
**Files:** API or database
**Steps:**
```bash
# Via API
curl http://localhost:5000/api/products/1/history

# Via database
sqlite3 data/products.db "SELECT * FROM price_history WHERE product_id = 1;"
```

## 📊 Project Structure

```
cj-black-friday-alerts/
│
├── 📝 Documentation (You are here)
│   ├── INDEX.md              ← Navigation (this file)
│   ├── PROJECT_SUMMARY.md    ← Overview
│   ├── README.md             ← Complete guide
│   ├── QUICKSTART.md         ← Quick setup
│   ├── DEPLOYMENT.md         ← Production guide
│   └── SYSTEM_OVERVIEW.md    ← Architecture
│
├── 💻 Core Application
│   ├── database.py           ← Database layer
│   ├── scraper.py            ← Scraping engine
│   ├── tracker.py            ← Orchestration
│   └── app.py                ← Flask API
│
├── 🔧 Configuration
│   ├── init_products.py      ← Product URLs
│   ├── requirements.txt      ← Dependencies
│   └── scheduler.sh          ← Cron script
│
├── 🎨 Frontend
│   └── static/
│       └── dashboard.html    ← Web UI
│
├── 🧪 Testing
│   └── test_scraper.py       ← Test script
│
└── 📦 Data (auto-created)
    ├── data/
    │   └── products.db       ← SQLite database
    └── logs/
        └── tracker-*.log     ← Daily logs
```

## 🆘 Support

### Getting Help

1. **Documentation:** Check relevant `.md` file above
2. **Logs:** Review `logs/tracker-YYYY-MM-DD.log`
3. **Database:** Inspect with `sqlite3 data/products.db`
4. **API:** Test with `curl http://localhost:5000/api/health`
5. **Testing:** Run `python test_scraper.py`

### Common Questions

**Q: How do I add more products?**
A: Edit `init_products.py` and run `python init_products.py`

**Q: How do I change the schedule?**
A: Edit crontab with `crontab -e`

**Q: How do I deploy to production?**
A: See [DEPLOYMENT.md](DEPLOYMENT.md)

**Q: How do I fix scraping errors?**
A: Check [README.md](README.md) troubleshooting section

**Q: How do I view price history?**
A: Use API endpoint `/api/products/:id/history`

## 📈 Version Information

- **Current Version:** v1.0.0
- **Release Date:** November 2024
- **Python Version:** 3.8+
- **Platform Support:** macOS, Linux, Windows

## 🔗 Quick Links

- **Dashboard:** http://localhost:5000
- **API Docs:** See [README.md](README.md#api-reference)
- **Database Schema:** See [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md#data-flow)
- **Deployment Options:** See [DEPLOYMENT.md](DEPLOYMENT.md#deployment-options)

---

**Need help?** Start with the document that matches your role above, or follow the "First Time Setup" reading order.

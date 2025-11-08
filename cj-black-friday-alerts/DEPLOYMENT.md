# Production Deployment Guide

This guide covers deploying the Black Friday tracker for 24/7 operation.

## Deployment Options

### Option 1: Local Machine (Simplest)

**Pros:**
- No hosting costs
- Full control
- Easy debugging

**Cons:**
- Computer must stay on
- No remote access (unless configured)

**Setup:**

```bash
# 1. Install as scheduled task (macOS/Linux)
crontab -e
# Add: 0 8 * * * /path/to/scheduler.sh

# 2. Run dashboard in background
nohup python app.py > dashboard.log 2>&1 &

# 3. Access locally
# Dashboard: http://localhost:5000
```

### Option 2: Raspberry Pi / Home Server

**Pros:**
- Low power consumption
- Always-on
- Affordable ($35-75)

**Cons:**
- Initial hardware investment
- Requires basic Linux knowledge

**Setup:**

```bash
# 1. Install Python 3
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 2. Clone project
git clone <repository> /home/pi/black-friday-tracker
cd /home/pi/black-friday-tracker

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Initialize
python init_products.py

# 5. Create systemd service for dashboard
sudo nano /etc/systemd/system/black-friday-tracker.service
```

**systemd service file:**
```ini
[Unit]
Description=Black Friday Price Tracker Dashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/black-friday-tracker
Environment="PATH=/home/pi/black-friday-tracker/venv/bin"
ExecStart=/home/pi/black-friday-tracker/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable service:**
```bash
sudo systemctl enable black-friday-tracker
sudo systemctl start black-friday-tracker
sudo systemctl status black-friday-tracker

# Add cron job
crontab -e
# Add: 0 8 * * * /home/pi/black-friday-tracker/scheduler.sh
```

### Option 3: Cloud VPS (DigitalOcean, Linode, AWS)

**Pros:**
- Always accessible
- Professional uptime
- Scalable

**Cons:**
- Monthly cost ($5-10)
- Requires server management

**Setup (Ubuntu 22.04):**

```bash
# 1. Connect to server
ssh root@your-server-ip

# 2. Update system
apt update && apt upgrade -y

# 3. Install Python
apt install python3 python3-pip python3-venv nginx -y

# 4. Create user
adduser tracker
usermod -aG sudo tracker
su - tracker

# 5. Clone and setup
git clone <repository> ~/black-friday-tracker
cd ~/black-friday-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn

# 6. Initialize
python init_products.py

# 7. Configure Gunicorn
cat > gunicorn_config.py << EOF
bind = "127.0.0.1:5000"
workers = 2
worker_class = "sync"
timeout = 120
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
EOF

# 8. Create systemd service
sudo nano /etc/systemd/system/black-friday-tracker.service
```

**systemd service:**
```ini
[Unit]
Description=Black Friday Price Tracker
After=network.target

[Service]
Type=notify
User=tracker
Group=tracker
WorkingDirectory=/home/tracker/black-friday-tracker
Environment="PATH=/home/tracker/black-friday-tracker/venv/bin"
ExecStart=/home/tracker/black-friday-tracker/venv/bin/gunicorn \
    --config gunicorn_config.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable service:**
```bash
sudo systemctl enable black-friday-tracker
sudo systemctl start black-friday-tracker
```

**Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/black-friday-tracker
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or server IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/black-friday-tracker \
            /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Add cron job as tracker user
crontab -e
# Add: 0 8 * * * /home/tracker/black-friday-tracker/scheduler.sh
```

**Access dashboard:**
```
http://your-server-ip
# or
http://your-domain.com
```

### Option 4: Docker Container

**Pros:**
- Portable
- Consistent environment
- Easy updates

**Setup:**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create data directory
RUN mkdir -p data logs

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  tracker:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: always
    environment:
      - DEBUG=False
```

**Deploy:**
```bash
# Build and run
docker-compose up -d

# Initialize database
docker-compose exec tracker python init_products.py

# View logs
docker-compose logs -f

# Add cron job on host machine
crontab -e
# Add: 0 8 * * * docker exec tracker_tracker_1 python tracker.py
```

## Security Considerations

### 1. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS (if using SSL)
sudo ufw enable
```

### 2. SSL/HTTPS (Production)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### 3. Database Backups

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/tracker/backups"
DATE=$(date +%Y-%m-%d)
mkdir -p "$BACKUP_DIR"
cp data/products.db "$BACKUP_DIR/products-$DATE.db"
# Keep only last 30 days
find "$BACKUP_DIR" -name "products-*.db" -mtime +30 -delete
EOF

chmod +x backup.sh

# Add to cron (daily at 2am)
crontab -e
# Add: 0 2 * * * /home/tracker/black-friday-tracker/backup.sh
```

### 4. Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/black-friday-tracker
```

```
/home/tracker/black-friday-tracker/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

## Monitoring

### Health Check Script

```bash
cat > healthcheck.sh << 'EOF'
#!/bin/bash
# Check if dashboard is responding
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "✅ Dashboard is healthy"
else
    echo "❌ Dashboard is down, restarting..."
    sudo systemctl restart black-friday-tracker
fi
EOF

chmod +x healthcheck.sh

# Run every 5 minutes
crontab -e
# Add: */5 * * * * /home/tracker/black-friday-tracker/healthcheck.sh
```

### Email Notifications

Install mailutils:
```bash
sudo apt install mailutils
```

Modify `scheduler.sh` to send email on new sales:
```bash
# Add at end of scheduler.sh
if grep -q "NEW SALES" "$LOG_FILE"; then
    mail -s "🔥 Black Friday Sale Alert!" your-email@example.com < "$LOG_FILE"
fi
```

## Performance Optimization

### 1. Increase Workers (for more products)

Edit `tracker.py`:
```python
track_all_products(max_workers=10)  # Increase from 3
```

### 2. Database Optimization

```bash
# Vacuum database monthly
echo "0 3 1 * * sqlite3 /path/to/data/products.db 'VACUUM;'" | crontab -
```

### 3. Caching (for high-traffic dashboard)

Install Redis:
```bash
sudo apt install redis-server
pip install flask-caching
```

Update `app.py`:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/products')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_products():
    # ... existing code
```

## Troubleshooting

### Dashboard won't start

```bash
# Check if port is in use
sudo netstat -tlnp | grep 5000

# Check service status
sudo systemctl status black-friday-tracker

# View logs
sudo journalctl -u black-friday-tracker -n 50
```

### Tracker not running via cron

```bash
# Check cron logs
grep CRON /var/log/syslog

# Test scheduler manually
./scheduler.sh

# Ensure absolute paths in crontab
```

### Database locked errors

```bash
# Reduce concurrent workers in tracker.py
# Or migrate to PostgreSQL

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib
pip install psycopg2-binary

# Update database.py to use PostgreSQL connection
```

## Scaling

### For 500+ Products

1. **Use PostgreSQL instead of SQLite**
2. **Increase workers**: `max_workers=20`
3. **Distribute scraping**: Multiple machines
4. **Use Redis for caching**

### For Multiple Users

1. **Add authentication**
2. **Use Nginx reverse proxy**
3. **Rate limit API endpoints**
4. **Monitor server resources**

## Cost Estimates

- **Local/Raspberry Pi**: $0-75 one-time
- **VPS (DigitalOcean/Linode)**: $5-10/month
- **AWS EC2 t3.micro**: ~$8/month
- **Cloud hosting with domain**: $15-20/month

## Recommended Setup

**For personal use:**
- Local machine or Raspberry Pi
- Free, no hosting needed

**For sharing with friends/family:**
- VPS (DigitalOcean $5 droplet)
- Nginx + SSL
- ~$60/year

**For production service:**
- Cloud VPS with backups
- Domain name
- SSL certificate
- Monitoring
- ~$150/year

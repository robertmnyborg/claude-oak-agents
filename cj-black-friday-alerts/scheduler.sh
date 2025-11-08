#!/bin/bash
#
# Black Friday Price Tracker - Cron Job Scheduler
# Runs daily price checks at 8am PST
#
# Installation:
#   chmod +x scheduler.sh
#   crontab -e
#   Add line: 0 8 * * * /path/to/scheduler.sh
#
# For 8am PST (adjust based on your server timezone):
#   If server is in PST: 0 8 * * *
#   If server is in EST: 0 11 * * *
#   If server is in UTC: 0 16 * * *

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Log file
LOG_FILE="$SCRIPT_DIR/logs/tracker-$(date +%Y-%m-%d).log"
mkdir -p "$SCRIPT_DIR/logs"

# Run tracker with logging
echo "========================================" >> "$LOG_FILE"
echo "Black Friday Tracker - $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

python3 tracker.py >> "$LOG_FILE" 2>&1

# Check exit code
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Tracking completed successfully" >> "$LOG_FILE"
else
    echo "❌ Tracking failed with exit code $EXIT_CODE" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# Optional: Send notification on new sales
# Uncomment and configure for email alerts
# if grep -q "NEW SALES" "$LOG_FILE"; then
#     # Send email notification
#     mail -s "🔥 Black Friday Sale Alert!" your-email@example.com < "$LOG_FILE"
# fi

exit $EXIT_CODE

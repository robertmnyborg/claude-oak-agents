# Automation Directory

Complete automation system for OaK agent continuous learning and improvement.

## Overview

This directory contains the automation infrastructure that:
1. **Prompts you** when reviews are due (shell integration)
2. **Runs reviews automatically** on schedule (launchd)
3. **Notifies you** when results are ready (macOS notifications)

## Quick Start

### Install Everything

```bash
cd ~/Projects/claude-oak-agents
./automation/install_automation.sh
```

The installer will guide you through:
- ✅ Shell prompt integration
- ✅ Scheduled task setup
- ✅ Notification system testing

### Manual Commands

After installation, these commands are available:

```bash
oak-status          # View system status
oak-weekly-review   # Run weekly analysis
oak-monthly-review  # Run monthly curation
oak-health-check    # Check system health
oak-dashboard       # View performance dashboard
```

## Components

### 1. Shell Prompts (`oak_prompts.sh`)

**Purpose:** Shows reminders when you open terminal

**How it works:**
- Sources in your `~/.zshrc`
- Checks last review dates
- Counts new agent invocations
- Shows prompt if action needed

**Example prompt:**
```
╔════════════════════════════════════════════════════════════╗
║          OaK Agent System - Action Required            ║
╚════════════════════════════════════════════════════════════╝

📊 Weekly OaK Review Due
   15 new agent invocations since last review
   Run: oak-weekly-review

💡 Tip: Reviews help the system learn and improve agent selection
```

**State Tracking:**
- Stores last review dates in `telemetry/.oak_review_state`
- Counts invocations since last review
- Only prompts when there's actionable data

### 2. Notification Wrapper (`oak_notify.sh`)

**Purpose:** Runs scripts and sends macOS notifications

**Commands:**
```bash
./automation/oak_notify.sh weekly   # Run weekly review
./automation/oak_notify.sh monthly  # Run monthly analysis
./automation/oak_notify.sh health   # Run health check
./automation/oak_notify.sh check    # Check for actionable data
./automation/oak_notify.sh test     # Test notification
```

**Features:**
- Runs scripts in background
- Captures output and errors
- Sends notifications on completion/failure
- Logs to `logs/automation.log`

**Notifications:**
- ✅ Success: "Review complete" (Glass sound)
- ⚠️  Warning: "Some checks failed" (Purr sound)
- ❌ Error: "Review failed" (Basso sound)

### 3. LaunchD Scheduled Tasks

**Purpose:** Automatically runs reviews on schedule

**Installed Jobs:**

| Job | Schedule | Purpose |
|-----|----------|---------|
| `com.oak.weekly-review` | Mondays 9am | Weekly performance analysis |
| `com.oak.monthly-analysis` | 1st of month 10am | Monthly curation agenda |
| `com.oak.health-check` | Every 3 days | System health validation |
| `com.oak.actionable-check` | Daily 9am | Check for pending reviews |

**Management:**
```bash
# List OaK jobs
launchctl list | grep com.oak

# View job details
launchctl print gui/$(id -u)/com.oak.weekly-review

# Unload job (disable)
launchctl unload ~/Library/LaunchAgents/com.oak.weekly-review.plist

# Load job (enable)
launchctl load ~/Library/LaunchAgents/com.oak.weekly-review.plist

# Start job manually (test)
launchctl start com.oak.weekly-review
```

**Logs:**
- Standard output: `logs/weekly-review.log`
- Errors: `logs/weekly-review.error.log`

## Workflow

### Daily (Automated)

1. **9am:** System checks for actionable data
2. If reviews due: Notification sent
3. You see notification or shell prompt
4. Run review command when convenient

### Weekly (Automated)

1. **Monday 9am:** Weekly review runs automatically
2. Generates report: `reports/weekly_report_YYYY-MM-DD.html`
3. Notification: "Weekly review complete"
4. Open terminal to view or run `oak-weekly-review` again

### Monthly (Automated)

1. **1st of month 10am:** Monthly analysis runs
2. Generates curation agenda: `reports/curation/agenda_YYYY-MM.md`
3. Notification: "Monthly analysis complete"
4. Review agenda and make curation decisions

### Every 3 Days (Automated)

1. Health check runs automatically
2. Only notifies if warnings/errors found
3. Run `oak-health-check` to see details

## State Management

### Review State File

**Location:** `telemetry/.oak_review_state`

**Contents:**
```
LAST_WEEKLY_REVIEW=2025-10-16
LAST_MONTHLY_REVIEW=2025-10-01
LAST_HEALTH_CHECK=2025-10-15
```

**Updated by:**
- `oak-weekly-review` command
- `oak-monthly-review` command
- `oak-health-check` command

### Why State Tracking?

Prevents spam:
- Only prompts when sufficient new data collected
- Only notifies when reviews are actually due
- Tracks when you last took action

## Customization

### Change Schedule

Edit plist files in `automation/launchd/`:

```xml
<!-- Change weekly to Wednesdays at 2pm -->
<key>StartCalendarInterval</key>
<dict>
    <key>Weekday</key>
    <integer>3</integer>  <!-- Wednesday -->
    <key>Hour</key>
    <integer>14</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.oak.weekly-review.plist
launchctl load ~/Library/LaunchAgents/com.oak.weekly-review.plist
```

### Change Notification Sound

Edit `oak_notify.sh`:

```bash
# Available sounds: Basso, Blow, Bottle, Frog, Funk, Glass, Hero,
#                   Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink
send_notification \
    "Title" \
    "Message" \
    "Submarine"  # Change sound here
```

### Adjust Review Thresholds

Edit `oak_prompts.sh`:

```bash
# Change weekly due from 6 days to 5 days
oak_is_weekly_due() {
    ...
    [ $days_since -ge 5 ]  # Was 6
}

# Require minimum invocations for monthly
oak_is_monthly_due() {
    ...
    if [ $new_invocations -gt 10 ]; then  # Was 5
        ...
    fi
}
```

## Troubleshooting

### Shell Prompts Not Showing

**Check if sourced:**
```bash
grep "oak_prompts.sh" ~/.zshrc
```

**Manually source:**
```bash
source ~/Projects/claude-oak-agents/automation/oak_prompts.sh
```

**Test prompt:**
```bash
oak_show_prompt
```

### Scheduled Tasks Not Running

**Check if loaded:**
```bash
launchctl list | grep com.oak
```

**Check logs:**
```bash
cat ~/Projects/claude-oak-agents/logs/weekly-review.error.log
```

**Manually trigger:**
```bash
launchctl start com.oak.weekly-review
```

**Common issues:**
- Path wrong in plist (check `ProgramArguments`)
- Python not in PATH for launchd
- Environment variables not set

### Notifications Not Appearing

**Test notifications:**
```bash
./automation/oak_notify.sh test
```

**Check System Preferences:**
- System Preferences > Notifications
- Find "Script Editor" or "Terminal"
- Enable notifications

**Alternative: Terminal notifications**
```bash
# In oak_notify.sh, replace osascript with terminal-notifier
# brew install terminal-notifier
terminal-notifier -message "Hello" -title "OaK"
```

### State File Corrupted

**Reset state:**
```bash
rm telemetry/.oak_review_state
source automation/oak_prompts.sh
oak_init_state
```

## Uninstallation

### Remove Shell Integration

Edit `~/.zshrc` and remove:
```bash
# OaK Agent System - Automated Prompts
source "/.../claude-oak-agents/automation/oak_prompts.sh"
```

### Remove Scheduled Tasks

```bash
cd ~/Library/LaunchAgents

# Unload and remove each job
launchctl unload com.oak.weekly-review.plist
launchctl unload com.oak.monthly-analysis.plist
launchctl unload com.oak.health-check.plist
launchctl unload com.oak.actionable-check.plist

rm com.oak.*.plist
```

### Remove State Files

```bash
rm ~/Projects/claude-oak-agents/telemetry/.oak_review_state
rm ~/Projects/claude-oak-agents/logs/*.log
```

## Advanced Usage

### Custom Notification Actions

Add action buttons to notifications (requires `terminal-notifier`):

```bash
terminal-notifier \
    -message "Weekly review ready" \
    -title "OaK System" \
    -execute "oak-weekly-review" \
    -sender com.apple.Terminal
```

### Slack Integration

Replace macOS notifications with Slack:

```bash
# In oak_notify.sh
send_slack_notification() {
    local webhook="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    local message=$1

    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"$message\"}" \
        "$webhook"
}
```

### Email Notifications

Send email instead of notifications:

```bash
# In oak_notify.sh
send_email_notification() {
    local subject=$1
    local body=$2

    echo "$body" | mail -s "$subject" your-email@example.com
}
```

## See Also

- [6-Month Deployment Plan](../docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)
- [Quick Start Guide](../QUICK_START.md)
- [Weekly Review Script](../scripts/automation/weekly_review.py)
- [Monthly Analysis Script](../scripts/automation/monthly_analysis.py)

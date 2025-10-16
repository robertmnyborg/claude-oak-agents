#!/bin/bash
# OaK Agent System - Notification Wrapper
# Sends macOS notifications and logs results

OAK_PROJECT_DIR="$HOME/Projects/claude-oak-agents"
OAK_STATE_DIR="${OAK_TELEMETRY_DIR:-$OAK_PROJECT_DIR/telemetry}"
OAK_LOG_DIR="$OAK_PROJECT_DIR/logs"

mkdir -p "$OAK_LOG_DIR"

# Function to send macOS notification
send_notification() {
    local title="$1"
    local message="$2"
    local sound="${3:-default}"

    osascript -e "display notification \"$message\" with title \"$title\" sound name \"$sound\""
}

# Function to log message
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")

    echo "[$timestamp] [$level] $message" >> "$OAK_LOG_DIR/automation.log"
}

# Run weekly review and notify
run_weekly_review() {
    log_message "INFO" "Starting weekly review"

    cd "$OAK_PROJECT_DIR"
    output=$(python3 scripts/automation/weekly_review.py 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log_message "INFO" "Weekly review completed successfully"

        # Count invocations for notification
        local report_file="reports/weekly_report_$(date +%Y-%m-%d).html"
        if [ -f "$report_file" ]; then
            send_notification \
                "OaK Weekly Review Complete" \
                "Review report generated. Run 'open $report_file' to view." \
                "Glass"
        else
            send_notification \
                "OaK Weekly Review Complete" \
                "Run 'oak-weekly-review' to view results." \
                "Glass"
        fi
    else
        log_message "ERROR" "Weekly review failed: $output"
        send_notification \
            "OaK Weekly Review Failed" \
            "Check logs: $OAK_LOG_DIR/automation.log" \
            "Basso"
    fi
}

# Run monthly analysis and notify
run_monthly_analysis() {
    log_message "INFO" "Starting monthly analysis"

    cd "$OAK_PROJECT_DIR"
    output=$(python3 scripts/automation/monthly_analysis.py 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log_message "INFO" "Monthly analysis completed successfully"

        send_notification \
            "OaK Monthly Analysis Complete" \
            "Curation agenda ready for review. Run 'oak-monthly-review' to view." \
            "Glass"
    else
        log_message "ERROR" "Monthly analysis failed: $output"
        send_notification \
            "OaK Monthly Analysis Failed" \
            "Check logs: $OAK_LOG_DIR/automation.log" \
            "Basso"
    fi
}

# Run health check and notify
run_health_check() {
    log_message "INFO" "Starting health check"

    cd "$OAK_PROJECT_DIR"
    output=$(python3 scripts/automation/health_check.py 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        log_message "INFO" "Health check passed"

        # Only notify if there are warnings
        if echo "$output" | grep -q "⚠️"; then
            send_notification \
                "OaK Health Check - Warnings" \
                "Some checks have warnings. Run 'oak-health-check' for details." \
                "Purr"
        fi
    else
        log_message "ERROR" "Health check failed: $output"
        send_notification \
            "OaK Health Check Failed" \
            "System health issues detected. Run 'oak-health-check' for details." \
            "Basso"
    fi
}

# Check for actionable data and notify
check_actionable_data() {
    log_message "INFO" "Checking for actionable data"

    cd "$OAK_PROJECT_DIR"

    # Source the prompts to use utility functions
    source "$OAK_PROJECT_DIR/automation/oak_prompts.sh"

    local has_actionable=false
    local message=""

    # Check for pending agent reviews
    local pending_count=$(ls -1 "$OAK_PROJECT_DIR/agents/pending_review"/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$pending_count" -gt 0 ]; then
        has_actionable=true
        message="$pending_count new agent(s) awaiting approval"
    fi

    # Check weekly review status
    if oak_is_weekly_due; then
        local last_weekly=$(oak_get_last_date "LAST_WEEKLY_REVIEW")
        local new_invocations=$(oak_count_new_invocations "$last_weekly")

        if [ $new_invocations -gt 0 ]; then
            has_actionable=true
            if [ -n "$message" ]; then
                message="$message. Weekly review due: $new_invocations invocations"
            else
                message="Weekly review due: $new_invocations new invocations"
            fi
        fi
    fi

    # Check monthly review status
    if oak_is_monthly_due; then
        local last_monthly=$(oak_get_last_date "LAST_MONTHLY_REVIEW")
        local new_invocations=$(oak_count_new_invocations "$last_monthly")

        if [ $new_invocations -gt 5 ]; then
            has_actionable=true
            if [ -n "$message" ]; then
                message="$message. Monthly analysis also due: $new_invocations invocations"
            else
                message="Monthly analysis due: $new_invocations invocations"
            fi
        fi
    fi

    # Send notification if actionable
    if [ "$has_actionable" = true ]; then
        log_message "INFO" "Actionable data found: $message"
        send_notification \
            "OaK System - Action Required" \
            "$message. Open terminal to review." \
            "Purr"
    else
        log_message "INFO" "No actionable data at this time"
    fi
}

# Notify about new agent for review
notify_new_agent() {
    local agent_name="$1"

    log_message "INFO" "Notifying about new agent: $agent_name"

    send_notification \
        "OaK - New Agent Created" \
        "Agent '$agent_name' ready for review. Run: oak-review-agent $agent_name" \
        "Glass"
}

# Main command dispatcher
case "${1:-help}" in
    weekly)
        run_weekly_review
        ;;
    monthly)
        run_monthly_analysis
        ;;
    health)
        run_health_check
        ;;
    check)
        check_actionable_data
        ;;
    agent)
        if [ -z "$2" ]; then
            echo "Usage: $0 agent <agent-name>"
            exit 1
        fi
        notify_new_agent "$2"
        ;;
    test)
        send_notification "OaK Test Notification" "If you see this, notifications are working!" "Glass"
        log_message "INFO" "Test notification sent"
        ;;
    help|*)
        echo "OaK Notification System"
        echo ""
        echo "Usage: $0 {weekly|monthly|health|check|agent|test}"
        echo ""
        echo "Commands:"
        echo "  weekly  - Run weekly review and notify"
        echo "  monthly - Run monthly analysis and notify"
        echo "  health  - Run health check and notify"
        echo "  check   - Check for actionable data and notify"
        echo "  agent <name> - Notify about new agent for review"
        echo "  test    - Send test notification"
        ;;
esac

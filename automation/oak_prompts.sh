#!/bin/bash
# OaK Agent System - Shell Prompt Integration
# Add to ~/.zshrc: source ~/Projects/claude-oak-agents/automation/oak_prompts.sh

OAK_STATE_DIR="${OAK_TELEMETRY_DIR:-$HOME/Projects/claude-oak-agents/telemetry}"
OAK_STATE_FILE="$OAK_STATE_DIR/.oak_review_state"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Initialize state file if it doesn't exist
oak_init_state() {
    if [ ! -f "$OAK_STATE_FILE" ]; then
        mkdir -p "$OAK_STATE_DIR"
        cat > "$OAK_STATE_FILE" <<EOF
LAST_WEEKLY_REVIEW=1970-01-01
LAST_MONTHLY_REVIEW=1970-01-01
LAST_HEALTH_CHECK=1970-01-01
EOF
    fi
}

# Get last review date
oak_get_last_date() {
    local key=$1
    if [ -f "$OAK_STATE_FILE" ]; then
        grep "^${key}=" "$OAK_STATE_FILE" | cut -d'=' -f2
    else
        echo "1970-01-01"
    fi
}

# Update last review date
oak_update_date() {
    local key=$1
    local date=$2
    oak_init_state

    # Update or add the key
    if grep -q "^${key}=" "$OAK_STATE_FILE"; then
        sed -i.bak "s/^${key}=.*/${key}=${date}/" "$OAK_STATE_FILE"
    else
        echo "${key}=${date}" >> "$OAK_STATE_FILE"
    fi
}

# Check if review is due
oak_is_weekly_due() {
    local last_review=$(oak_get_last_date "LAST_WEEKLY_REVIEW")
    local days_since=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$last_review" +%s 2>/dev/null || echo 0)) / 86400 ))

    # Due if more than 6 days since last review
    [ $days_since -ge 6 ]
}

oak_is_monthly_due() {
    local last_review=$(oak_get_last_date "LAST_MONTHLY_REVIEW")
    local days_since=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$last_review" +%s 2>/dev/null || echo 0)) / 86400 ))

    # Due if more than 28 days since last review
    [ $days_since -ge 28 ]
}

oak_is_health_check_due() {
    local last_check=$(oak_get_last_date "LAST_HEALTH_CHECK")
    local days_since=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$last_check" +%s 2>/dev/null || echo 0)) / 86400 ))

    # Due if more than 2 days since last check
    [ $days_since -ge 3 ]
}

# Count invocations since last review
oak_count_new_invocations() {
    local since_date=$1
    local invocations_file="$OAK_STATE_DIR/agent_invocations.jsonl"

    if [ ! -f "$invocations_file" ]; then
        echo 0
        return
    fi

    # Count lines with timestamp after since_date
    local since_epoch=$(date -j -f "%Y-%m-%d" "$since_date" +%s 2>/dev/null || echo 0)
    local count=0

    while IFS= read -r line; do
        local timestamp=$(echo "$line" | grep -o '"timestamp":[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
        if [ -n "$timestamp" ]; then
            # Remove microseconds and Z suffix: 2025-10-19T15:31:47.887917Z -> 2025-10-19T15:31:47
            local clean_timestamp=$(echo "$timestamp" | sed 's/\.[0-9]*Z$//' | sed 's/Z$//')
            local line_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$clean_timestamp" +%s 2>/dev/null || echo 0)
            if [ $line_epoch -gt $since_epoch ]; then
                count=$((count + 1))
            fi
        fi
    done < "$invocations_file"

    echo $count
}

# Main prompt function - called on shell startup
oak_show_prompt() {
    # Only show prompts if telemetry is enabled
    if [ "${OAK_TELEMETRY_ENABLED:-true}" != "true" ]; then
        return
    fi

    oak_init_state

    local show_prompt=false
    local messages=""

    # Check for weekly review
    if oak_is_weekly_due; then
        local last_weekly=$(oak_get_last_date "LAST_WEEKLY_REVIEW")
        local new_invocations=$(oak_count_new_invocations "$last_weekly")

        if [ $new_invocations -gt 0 ]; then
            show_prompt=true
            messages="${messages}\n${YELLOW}📊 Weekly OaK Review Due${NC}"
            messages="${messages}\n   ${new_invocations} new agent invocations since last review"
            messages="${messages}\n   ${BLUE}Run:${NC} oak-weekly-review"
        fi
    fi

    # Check for monthly review
    if oak_is_monthly_due; then
        local last_monthly=$(oak_get_last_date "LAST_MONTHLY_REVIEW")
        local new_invocations=$(oak_count_new_invocations "$last_monthly")

        if [ $new_invocations -gt 5 ]; then
            show_prompt=true
            messages="${messages}\n${YELLOW}📈 Monthly OaK Analysis Due${NC}"
            messages="${messages}\n   ${new_invocations} new invocations for curation analysis"
            messages="${messages}\n   ${BLUE}Run:${NC} oak-monthly-review"
        fi
    fi

    # Check for health check
    if oak_is_health_check_due; then
        show_prompt=true
        messages="${messages}\n${BLUE}🏥 System Health Check Recommended${NC}"
        messages="${messages}\n   ${BLUE}Run:${NC} oak-health-check"
    fi

    # Check for pending agent reviews
    local pending_count=$(ls -1 ~/Projects/claude-oak-agents/agents/pending_review/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$pending_count" -gt 0 ]; then
        show_prompt=true
        messages="${messages}\n${YELLOW}🤖 ${pending_count} New Agent(s) Awaiting Approval${NC}"
        messages="${messages}\n   Auto-created agents need your review before deployment"
        messages="${messages}\n   ${BLUE}Run:${NC} oak-list-pending-agents"
    fi

    # Show consolidated prompt
    if [ "$show_prompt" = true ]; then
        echo -e "\n${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BOLD}║          OaK Agent System - Action Required            ║${NC}"
        echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
        echo -e "$messages"
        echo -e "\n${GREEN}💡 Tip:${NC} Reviews help the system learn and improve agent selection"
        echo ""
    fi
}

# Helper commands for manual execution
oak-weekly-review() {
    echo -e "${BLUE}Running weekly review...${NC}\n"
    cd ~/Projects/claude-oak-agents
    python3 scripts/automation/weekly_review.py

    if [ $? -eq 0 ]; then
        oak_update_date "LAST_WEEKLY_REVIEW" "$(date +%Y-%m-%d)"
        echo -e "\n${GREEN}✓ Review complete! Updated: $(date +%Y-%m-%d)${NC}"

        # Open report if it exists
        local report_file="reports/weekly_report_$(date +%Y-%m-%d).html"
        if [ -f "$report_file" ]; then
            echo -e "${BLUE}Opening report...${NC}"
            open "$report_file"
        fi
    fi
}

oak-monthly-review() {
    echo -e "${BLUE}Running monthly analysis...${NC}\n"
    cd ~/Projects/claude-oak-agents
    python3 scripts/automation/monthly_analysis.py

    if [ $? -eq 0 ]; then
        oak_update_date "LAST_MONTHLY_REVIEW" "$(date +%Y-%m-%d)"
        echo -e "\n${GREEN}✓ Analysis complete! Updated: $(date +%Y-%m-%d)${NC}"

        # Open report if it exists
        local report_file="reports/curation/agenda_$(date +%Y-%m).md"
        if [ -f "$report_file" ]; then
            echo -e "${BLUE}Opening curation agenda...${NC}"
            open "$report_file"
        fi
    fi
}

oak-health-check() {
    echo -e "${BLUE}Running system health check...${NC}\n"
    cd ~/Projects/claude-oak-agents
    python3 scripts/automation/health_check.py

    oak_update_date "LAST_HEALTH_CHECK" "$(date +%Y-%m-%d)"
    echo -e "\n${GREEN}✓ Health check complete!${NC}"
}

oak-dashboard() {
    echo -e "${BLUE}Generating performance dashboard...${NC}\n"
    cd ~/Projects/claude-oak-agents
    python3 scripts/phase4/generate_dashboard.py

    if [ $? -eq 0 ]; then
        local report_file="reports/dashboard_$(date +%Y-%m-%d).html"
        if [ -f "$report_file" ]; then
            echo -e "${GREEN}✓ Dashboard generated!${NC}"
            open "$report_file"
        fi
    fi
}

oak-status() {
    oak_init_state
    echo -e "${BOLD}OaK Agent System Status${NC}\n"

    local last_weekly=$(oak_get_last_date "LAST_WEEKLY_REVIEW")
    local last_monthly=$(oak_get_last_date "LAST_MONTHLY_REVIEW")
    local last_health=$(oak_get_last_date "LAST_HEALTH_CHECK")

    echo -e "${BLUE}Last Reviews:${NC}"
    echo -e "  Weekly:  $last_weekly"
    echo -e "  Monthly: $last_monthly"
    echo -e "  Health:  $last_health\n"

    local new_weekly=$(oak_count_new_invocations "$last_weekly")
    local new_monthly=$(oak_count_new_invocations "$last_monthly")

    echo -e "${BLUE}New Invocations:${NC}"
    echo -e "  Since weekly:  $new_weekly"
    echo -e "  Since monthly: $new_monthly\n"

    # Check for pending agent reviews
    local pending_count=$(ls -1 ~/Projects/claude-oak-agents/agents/pending_review/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$pending_count" -gt 0 ]; then
        echo -e "${YELLOW}Pending Agent Reviews:${NC}"
        echo -e "  ${pending_count} agent(s) awaiting approval\n"
    fi

    echo -e "${BLUE}Available Commands:${NC}"
    echo -e "  ${GREEN}oak-weekly-review${NC}  - Run weekly analysis"
    echo -e "  ${GREEN}oak-monthly-review${NC} - Run monthly curation"
    echo -e "  ${GREEN}oak-health-check${NC}   - Check system health"
    echo -e "  ${GREEN}oak-dashboard${NC}      - View performance dashboard"
    echo -e "  ${GREEN}oak-status${NC}         - Show this status\n"

    if [ "$pending_count" -gt 0 ]; then
        echo -e "${BLUE}Agent Review Commands:${NC}"
        echo -e "  ${GREEN}oak-list-pending-agents${NC} - List agents pending review"
        echo -e "  ${GREEN}oak-review-agent <name>${NC} - Review agent specification"
        echo -e "  ${GREEN}oak-approve-agent <name>${NC} - Approve and deploy agent"
    fi
}

# Agent Review Commands
oak-list-pending-agents() {
    cd ~/Projects/claude-oak-agents
    python3 scripts/agent_review.py list
}

oak-review-agent() {
    if [ -z "$1" ]; then
        echo "Usage: oak-review-agent <agent-name>"
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    python3 scripts/agent_review.py review "$1"
}

oak-approve-agent() {
    if [ -z "$1" ]; then
        echo "Usage: oak-approve-agent <agent-name>"
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    python3 scripts/agent_review.py approve "$1"
}

oak-modify-agent() {
    if [ -z "$1" ]; then
        echo "Usage: oak-modify-agent <agent-name>"
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    python3 scripts/agent_review.py modify "$1"
}

oak-reject-agent() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: oak-reject-agent <agent-name> \"<reason>\""
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    python3 scripts/agent_review.py reject "$1" "$2"
}

oak-check-pending() {
    cd ~/Projects/claude-oak-agents
    python3 scripts/agent_review.py check
}

# Proposal Review Commands (Phase 2)
oak-review-proposals() {
    cd ~/Projects/claude-oak-agents
    python3 scripts/phase2/list_proposals.py
}

oak-review-proposal() {
    if [ -z "$1" ]; then
        echo "Usage: oak-review-proposal <agent-name>"
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    python3 scripts/phase2/review_proposal.py "$1"
}

oak-approve-proposal() {
    if [ -z "$1" ]; then
        echo "Usage: oak-approve-proposal <agent-name> [notes]"
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    if [ -n "$2" ]; then
        python3 scripts/phase2/approve_proposal.py "$1" "$2"
    else
        python3 scripts/phase2/approve_proposal.py "$1"
    fi
}

oak-reject-proposal() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: oak-reject-proposal <agent-name> \"<reason>\""
        return 1
    fi
    cd ~/Projects/claude-oak-agents
    python3 scripts/phase2/reject_proposal.py "$1" "$2"
}

oak-apply-improvements() {
    cd ~/Projects/claude-oak-agents
    python3 scripts/phase2/apply_improvements.py
}

# Workflow Coordination Commands (Phase 2)
oak-workflows() {
    echo "📊 Recent Multi-Agent Workflows"
    echo "========================================================================"

    OAK_ROOT="${OAK_ROOT:-$HOME/Projects/claude-oak-agents}"
    cd "$OAK_ROOT" || return 1

    if [ ! -f "telemetry/workflow_events.jsonl" ] || [ ! -s "telemetry/workflow_events.jsonl" ]; then
        echo "No workflow data yet (single-agent tasks only)"
        return 0
    fi

    python3 << 'EOF'
import sys
from pathlib import Path
import json
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()
stats = analyzer.analyze_workflows()

print(f"\nTotal Workflows: {stats['total_workflows']}")
print(f"Success Rate: {stats['success_rate']:.0%}")
print(f"Avg Duration: {stats['avg_duration_minutes']:.1f} minutes")
print(f"Avg Agents/Workflow: {stats['avg_agents_per_workflow']:.1f}")

if stats.get('most_common_patterns'):
    print(f"\nCommon Agent Patterns:")
    for pattern_data in stats['most_common_patterns'][:5]:
        pattern = pattern_data['pattern']
        count = pattern_data['count']
        print(f"  {pattern} ({count}x)")

overhead = analyzer.calculate_coordination_overhead()
print(f"\nCoordination Overhead: {overhead['coordination_overhead_pct']:.1f}%")
print(f"Recommendation: {overhead['recommendation']}")
EOF
}

oak-query-agent() {
    if [ -z "$1" ]; then
        echo "Usage: oak-query-agent \"task description\" [domain]"
        echo "Example: oak-query-agent \"API development\" backend"
        return 1
    fi

    local task="$1"
    local domain="${2:-}"

    OAK_ROOT="${OAK_ROOT:-$HOME/Projects/claude-oak-agents}"
    cd "$OAK_ROOT" || return 1

    if [ -n "$domain" ]; then
        python3 scripts/query_best_agent.py --task "$task" --domain "$domain"
    else
        python3 scripts/query_best_agent.py --task "$task"
    fi
}

oak-agent-trends() {
    if [ -z "$1" ]; then
        echo "Usage: oak-agent-trends <agent-name>"
        echo "Example: oak-agent-trends backend-architect"
        return 1
    fi

    local agent_name="$1"

    OAK_ROOT="${OAK_ROOT:-$HOME/Projects/claude-oak-agents}"
    cd "$OAK_ROOT" || return 1

    python3 << EOF
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from telemetry.analyzer import TelemetryAnalyzer

analyzer = TelemetryAnalyzer()
trend_data = analyzer.get_agent_performance_trends("$agent_name", days=30)

print(f"\n📈 Performance Trends: $agent_name")
print(f"=" * 60)
print(f"Trend: {trend_data['trend']}")
print(f"Recent Success Rate (7 days): {trend_data['recent_success_rate']:.0%}")
print(f"Historical Success Rate: {trend_data['historical_success_rate']:.0%}")
print(f"Change: {trend_data['success_rate_change']:+.1f} percentage points")
EOF
}

oak-analyze-workflow() {
    if [ -z "$1" ]; then
        echo "Usage: oak-analyze-workflow <workflow-id>"
        echo "       oak-analyze-workflow --list    # List all workflows"
        echo "       oak-analyze-workflow           # Analyze all workflows"
        return 1
    fi

    OAK_ROOT="${OAK_ROOT:-$HOME/Projects/claude-oak-agents}"
    cd "$OAK_ROOT" || return 1

    python3 scripts/phase3/analyze_workflow.py "$@"
}

oak-test-workflow-monitor() {
    echo "🧪 Testing Phase 3 Workflow Monitor..."
    OAK_ROOT="${OAK_ROOT:-$HOME/Projects/claude-oak-agents}"
    cd "$OAK_ROOT" || return 1

    python3 scripts/phase3/test_workflow_monitor.py
}

oak-help() {
    cat << 'EOF'
OaK Agent System Commands
======================================================================

Workflow Intelligence (Phase 3):
  oak-analyze-workflow <id>        Analyze specific workflow performance
  oak-analyze-workflow --list      List all workflows
  oak-analyze-workflow             Analyze all workflows (summary)
  oak-test-workflow-monitor        Test workflow monitoring system

Workflow Coordination (Phase 2):
  oak-workflows                    Show recent multi-agent workflow stats
  oak-query-agent "task" [domain]  Query best agent for a task
  oak-agent-trends <agent-name>    View agent performance trends

Weekly/Monthly Reviews:
  oak-weekly-review                Run weekly telemetry review
  oak-monthly-review               Run monthly agent portfolio audit
  oak-health-check                 Check system health

Agent Management:
  oak-list-pending-agents          List agents pending review
  oak-review-agent <name>          Review agent specification
  oak-approve-agent <name>         Approve and deploy agent
  oak-status                       Show overall system status

Improvement Proposals (Phase 2):
  oak-review-proposals             List pending improvement proposals
  oak-review-proposal <name>       Review specific proposal
  oak-approve-proposal <name>      Approve and queue proposal
  oak-reject-proposal <name> "reason"  Reject proposal
  oak-apply-improvements           Apply approved improvements

Documentation:
  oak-help                         Show this help message
EOF
}

# Show prompt on shell startup (only once per session)
if [ -z "$OAK_PROMPT_SHOWN" ]; then
    export OAK_PROMPT_SHOWN=1
    oak_show_prompt
fi

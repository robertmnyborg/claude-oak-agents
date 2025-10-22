#!/bin/bash
# Query workflow invocations by workflow_id

if [ -z "$1" ]; then
    echo "Usage: $0 <workflow_id>"
    echo "       $0 --list-today    # List today's workflows"
    echo "       $0 --list-all      # List all workflows"
    exit 1
fi

TELEMETRY_FILE="${OAK_TELEMETRY_DIR:-telemetry}/agent_invocations.jsonl"

if [ ! -f "$TELEMETRY_FILE" ]; then
    echo "Error: Telemetry file not found at $TELEMETRY_FILE"
    exit 1
fi

case "$1" in
    --list-today)
        TODAY=$(date +%Y-%m-%d)
        echo "Workflows from $TODAY:"
        echo ""
        jq -r "select(.workflow_id != null and (.timestamp | startswith(\"$TODAY\"))) | .workflow_id" \
            "$TELEMETRY_FILE" | sort -u
        ;;
    --list-all)
        echo "All workflows:"
        echo ""
        jq -r 'select(.workflow_id != null) | .workflow_id' \
            "$TELEMETRY_FILE" | sort -u
        ;;
    *)
        echo "Workflow: $1"
        echo ""
        echo -e "TIMESTAMP\tAGENT\tSTATUS\tDURATION"
        jq -r "select(.workflow_id == \"$1\") | 
            [.timestamp, .agent_name, .outcome.status, .duration_seconds] | 
            @tsv" \
            "$TELEMETRY_FILE" | 
            column -t -s $'\t'
        ;;
esac

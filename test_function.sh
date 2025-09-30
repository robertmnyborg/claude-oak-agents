#!/bin/bash

# Function to merge JSON files using jq
merge_json_files() {
    local existing_file="$1"
    local new_file="$2"
    local target_file="$3"

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        echo "⚠️  Warning: jq not found, copying without merging"
        cp "$new_file" "$target_file"
        return 1
    fi

    # If existing file doesn't exist, just copy the new one
    if [ ! -f "$existing_file" ]; then
        echo "📄 Creating new configuration file..."
        cp "$new_file" "$target_file"
        return 0
    fi

    # Merge files using jq
    echo "📄 Merging JSON configuration..."
    jq -s '.[0] * .[1]' "$existing_file" "$new_file" > "${target_file}.tmp"
    mv "${target_file}.tmp" "$target_file"
    echo "✅ Configuration merged successfully"
    return 0
}

# Test scenario 1: No existing file
echo '{"agents": {"enabled": true}, "new_feature": "test"}' > new_settings.json
merge_json_files "nonexistent.json" "new_settings.json" "result1.json"
echo "Result 1:"
cat result1.json
echo ""

# Test scenario 2: Merge with existing file
echo '{"user_setting": "keep_me", "agents": {"timeout": 30000}}' > existing_settings.json
merge_json_files "existing_settings.json" "new_settings.json" "result2.json"
echo "Result 2:"
cat result2.json
echo ""

# Test scenario 3: Complex merge
echo '{"feedbackSurveyState": {"lastShownTime": 1754085923371}, "statusLine": {"enabled": false}}' > user_settings.json
echo '{"statusLine": {"enabled": true, "format": "developer"}, "agents": {"enabled": true}}' > package_settings.json
merge_json_files "user_settings.json" "package_settings.json" "result3.json"
echo "Result 3:"
cat result3.json
echo ""

# Scripts Directory

Utility scripts for testing and demonstrating the OaK architecture.

## Test Scripts

### test_telemetry_e2e.py
End-to-end test of the telemetry system.

**What it does:**
1. Creates a temporary test workspace with sample Python files
2. Extracts state features from the workspace
3. Logs multiple agent invocations with different scenarios
4. Analyzes the logged telemetry data
5. Generates performance statistics

**Usage:**
```bash
python scripts/test_telemetry_e2e.py
```

**Expected output:**
- Test workspace created in `/tmp/oak_test_*`
- Telemetry data in `/tmp/oak_telemetry_*`
- All tests pass with green checkmarks

---

### test_state_analysis.py
Tests state feature extraction on the current project.

**What it does:**
1. Analyzes the claude-oak-agents project itself
2. Extracts codebase features (languages, frameworks, LOC, complexity)
3. Extracts context features (tests, docs, git status)
4. Provides recommendations based on state analysis
5. Saves full analysis to `state_analysis_output.json`

**Usage:**
```bash
python scripts/test_state_analysis.py
```

**Expected output:**
- Detailed breakdown of codebase features
- Context analysis (tests, docs, git state)
- Recommendations for agent selection
- JSON output saved to project root

---

### demo_workflow.py
Demonstrates the complete OaK workflow from start to finish.

**What it does:**
1. Defines a sample task (OAuth2 implementation)
2. Runs state analysis to extract features
3. Ranks features by importance
4. Recommends agents based on state
5. Simulates agent execution with telemetry logging
6. Generates performance analysis

**Usage:**
```bash
python scripts/demo_workflow.py
```

**Expected output:**
- Complete workflow demonstration
- Telemetry data generated in `/tmp/oak_demo_*`
- Performance statistics for all agents

---

## Analysis Scripts

### analyze_telemetry.sh
Bash wrapper for easy telemetry analysis.

**What it does:**
1. Checks for existing telemetry data
2. Runs the telemetry analyzer
3. Displays quick summary (if `jq` is installed)
4. Shows path to full statistics

**Usage:**
```bash
./scripts/analyze_telemetry.sh
```

**Requirements:**
- Telemetry data must exist in `telemetry/` directory
- Optional: `jq` for pretty JSON formatting

---

## Running All Tests

```bash
# Make sure scripts are executable
chmod +x scripts/*.py scripts/*.sh

# Run end-to-end test
python scripts/test_telemetry_e2e.py

# Run state analysis
python scripts/test_state_analysis.py

# Run workflow demo
python scripts/demo_workflow.py

# Analyze telemetry (after generating data)
./scripts/analyze_telemetry.sh
```

## Expected Results

All scripts should complete with exit code 0 and display:
- ✅ Green checkmarks for successful operations
- 📊 Statistics and analysis results
- 💾 Paths to generated files

If any script fails:
1. Check that you're in the project root directory
2. Verify Python 3.8+ is installed
3. Ensure all dependencies are available (standard library only)
4. Check file permissions

## Troubleshooting

### "ModuleNotFoundError" when running scripts
**Solution:** Add project root to PYTHONPATH:
```bash
export PYTHONPATH="/Users/robertnyborg/Projects/claude-oak-agents:$PYTHONPATH"
```

### "No telemetry data found"
**Solution:** Generate test data first:
```bash
python scripts/test_telemetry_e2e.py
# OR
python scripts/demo_workflow.py
```

### Scripts not executable
**Solution:**
```bash
chmod +x scripts/*.py scripts/*.sh
```

## Integration with Claude Code

These scripts can be used as reference implementations when:
- Testing the state-analyzer agent
- Validating telemetry infrastructure
- Demonstrating OaK workflows to team members
- Debugging agent selection logic

## Future Enhancements

Planned additions:
- [ ] Hook integration scripts (Phase 1.5)
- [ ] Performance benchmarking suite
- [ ] ML pipeline testing scripts (Phase 6)
- [ ] Dashboard generation scripts
- [ ] A/B testing framework

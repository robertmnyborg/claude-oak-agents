# Test Routing Fix - Enhanced Contextual Agent Selection

## Problem Solved
**Issue**: "Fix tests" was incorrectly routing to `programmer` agent instead of `qa-specialist` agent.

**Root Cause**: Simple keyword matching where "fix" triggered programming routing regardless of test context.

## Solution Implemented
Enhanced trigger-based routing in `CLAUDE.md` with priority-based contextual pattern recognition:

### Priority 1: Test-Specific Contextual Patterns
- **Test fixing patterns**: "fix tests", "debug tests", "repair tests", "troubleshoot tests"
- **Routes to**: qa-specialist agent
- **Unit test patterns**: "fix unit tests", "debug unit tests", "update unit tests"
- **Routes to**: unit-test-expert agent

### Priority 2: Specialist Domain Triggers
- Testing, infrastructure, security, analysis triggers

### Priority 3: General Programming Triggers
- General fix, implement, create triggers (lower priority)

### Contextual Override Rules
- **Test context wins**: Test-related words override general programming triggers
- **File path detection**: Automatic routing based on test file patterns
- **Compound phrase matching**: Multi-word phrases prioritized over single words

## Technical Details

### Enhanced Pattern Recognition
```
OLD: "fix" → programmer agent
NEW: "fix tests" → qa-specialist agent
NEW: "fix unit tests" → unit-test-expert agent
NEW: "fix failing tests" → qa-specialist agent
```

### File Path Detection
- test/, tests/, __tests__/ directories
- *.test.*, *.spec.* files
- cypress/, e2e/ directories
- Automatically routes to appropriate testing specialist

## Impact
- **Correct agent selection**: Test-related tasks now go to testing specialists
- **Improved efficiency**: Right specialist for the job means faster, better results
- **Better user experience**: Test fixes handled by qa-specialist with deep testing expertise
- **Maintained backwards compatibility**: General programming triggers still work for non-test contexts

## Validation
This fix addresses the real-world issue where users requesting test fixes were getting general programming help instead of specialized testing assistance.

The qa-specialist agent includes:
- Test framework expertise
- Test strategy and debugging
- Integration and e2e testing
- Test environment configuration
- Performance and accessibility testing

## Architecture Lesson
Simple keyword-based routing is insufficient for complex development workflows. Contextual pattern recognition with priority hierarchies provides more accurate agent selection while maintaining system simplicity.
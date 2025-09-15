# Orchestrator Recursion Test

## Test Scenarios

### 1. Simple Question (Should NOT trigger orchestrator)
- "What is 2+2?"
- "How do I list files?"
- "What does this code do?"

### 2. Code Changes (SHOULD trigger orchestrator)
- "Fix the bug in authentication.js"
- "Refactor the database connection code"
- "Add a new feature to handle user uploads"

### 3. Multi-Step Tasks (SHOULD trigger orchestrator)
- "Create a new React component with tests and documentation"
- "Set up CI/CD pipeline with testing and deployment"
- "Analyze performance, optimize, and document findings"

## Validation Checklist

✅ **PASS CONDITIONS:**
1. Orchestrator is invoked only for appropriate scenarios
2. Orchestrator output contains only valid JSON
3. No Task calls have `subagent_type: "agent-orchestrator"`
4. Re-invocation uses `next_steps` field, not Task calls
5. No infinite loops or recursion errors

❌ **FAIL CONDITIONS:**
1. Orchestrator calls itself via Task tool
2. Infinite recursion or memory overflow
3. Simple questions trigger orchestration
4. Complex tasks bypass orchestration

## Key Changes Made

### CLAUDE.md
- Changed from mandatory orchestration for ALL requests
- To selective orchestration for specific trigger scenarios
- Added clear list of when to invoke vs skip orchestration

### agent_orchestrator.md
- Updated invocation requirements from "every request" to "specific scenarios"
- Strengthened self-invocation prevention rules
- Added validation rules before creating Task calls
- Clarified correct pattern using `next_steps` field

## Expected Behavior

1. **Simple Request:** "What is Docker?"
   - Direct response, no orchestration

2. **Code Change Request:** "Fix the memory leak in server.js"
   - Triggers orchestrator
   - Orchestrator dispatches code-reviewer, debug-specialist, etc.
   - Uses `next_steps` for continuation
   - No self-invocation

3. **Complex Project:** "Build a REST API with authentication"
   - Triggers orchestrator
   - Dispatches project-manager, systems-architect
   - Coordinates multiple agents
   - No recursion issues
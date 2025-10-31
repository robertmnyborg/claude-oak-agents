# Quick Start: Agent Auto-Activation System

**Quick setup guide for the new auto-activation features**

---

## 5-Minute Quick Start

### Step 1: Verify Files Created ✓

Check that these files exist:
```bash
ls -la .claude/hooks/agent-activation-prompt.md
ls -la .claude/hooks/post-agent-execution.md
ls -la .claude/hooks/pre-commit-validation.md
ls -la .claude/agent-rules.json
ls -la .claude/AGENT_PATTERNS.md
ls -la .claude/TELEMETRY_INTEGRATION.md
```

### Step 2: Enable Hooks in Claude Code

The hooks should activate automatically when Claude Code loads your project. Verify by checking `.claude/hooks/` is recognized.

### Step 3: Test Auto-Activation

Try these test phrases to see agent suggestions:

**Test 1: Backend Work**
```
Prompt: "I need to design a database schema for user authentication"
Expected: Suggests backend-architect + security-auditor
```

**Test 2: Security Work**
```
Prompt: "Add OAuth2 authentication with JWT tokens"
Expected: Suggests design-simplicity-advisor + backend-architect + security-auditor
```

**Test 3: Debugging**
```
Prompt: "My API is returning 500 errors"
Expected: Suggests debug-specialist (highest priority)
```

**Test 4: Frontend Work**
```
Prompt: "Create a React dashboard with user analytics"
Expected: Suggests frontend-developer
```

**Test 5: No Suggestion (Simple Query)**
```
Prompt: "What does this function do?"
Expected: No agent suggestion (handled directly)
```

### Step 4: Test Pre-Commit Validation

```bash
# Make a change to multiple files
echo "// test" >> src/file1.ts
echo "// test" >> src/file2.ts
echo "// test" >> src/file3.ts

# Stage changes
git add src/*.ts

# Try to commit (should trigger validation)
git commit -m "Test pre-commit validation"

# Expected: Pre-commit hook runs code-reviewer
```

### Step 5: Check Telemetry

After running a few agent invocations:
```bash
# Check if telemetry is being logged
ls -la telemetry/suggestions/$(date +%Y-%m-%d)/
ls -la telemetry/invocations/$(date +%Y-%m-%d)/

# View a suggestion log
cat telemetry/suggestions/$(date +%Y-%m-%d)/sug-*.json | jq .

# View an invocation log
cat telemetry/invocations/$(date +%Y-%m-%d)/inv-*.json | jq .
```

---

## Common Usage Patterns

### Pattern 1: New Feature Implementation
```
You: "Build a payment processing system with Stripe"

System: 🤖 AGENT SUGGESTION
  - project-manager (complex multi-domain)
  - design-simplicity-advisor (validate approach)
  - backend-architect (API and database)
  - security-auditor (payment security)

You: "1" (activate agents)

[Agents execute in coordinated workflow]
```

### Pattern 2: Bug Fix
```
You: "Fix TypeError: Cannot read property 'user' of undefined"

System: 🤖 AGENT SUGGESTION
  - debug-specialist (HIGHEST PRIORITY for errors)

You: "1" (activate agent)

[debug-specialist diagnoses issue]
[Suggests backend-architect for fix if needed]
```

### Pattern 3: Code Review Before Commit
```
You: [Modified 5 files, ready to commit]
You: "git commit -m 'Add authentication'"

System: [pre-commit-validation hook]
  - Running code-reviewer (5 files)
  - Running security-auditor (auth files)
  - [Results display]

System: ✅ Pre-commit validation passed
  [Commit proceeds]
```

---

## Customization

### Adjust Confidence Thresholds

Edit `.claude/agent-rules.json`:

```json
{
  "name": "backend-architect",
  "confidence_threshold": 0.75  // Lower = more suggestions, Higher = fewer
}
```

Recommended thresholds:
- **Critical agents**: 0.70 (debug-specialist, security-auditor)
- **High priority**: 0.75 (backend-architect, frontend-developer)
- **Medium priority**: 0.80 (qa-specialist, performance-optimizer)

### Add Custom Keywords

Edit triggers in `.claude/agent-rules.json`:

```json
{
  "name": "backend-architect",
  "triggers": {
    "keywords": [
      "database", "schema", "API",
      "my-custom-keyword"  // Add your keywords
    ]
  }
}
```

### Disable Agent Auto-Activation

Set `auto_activate: false` in `.claude/agent-rules.json`:

```json
{
  "name": "agent-name",
  "auto_activate": false,  // Changed from true
  "triggers": { ... }
}
```

### Customize Pre-Commit Rules

Create `.claude/pre-commit-config.json`:

```json
{
  "validations": {
    "code_review": {
      "enabled": true,
      "blocking": true,
      "thresholds": {
        "file_count": 5,      // Changed from 3
        "lines_changed": 150  // Changed from 100
      }
    }
  }
}
```

---

## Understanding Agent Suggestions

### Confidence Levels

```
🟢 90-100% = Very High Confidence
   "I'm very sure you need this agent"

🟡 80-89% = High Confidence
   "This agent is likely relevant"

🟠 70-79% = Medium Confidence
   "This agent might be helpful"

🔴 60-69% = Low Confidence
   "Not sure, but could be relevant" (usually not suggested)
```

### Priority Levels

```
🔴 Critical = Must activate (debug, security, design review)
🟠 High = Should activate for domain work (backend, frontend, infra)
🟡 Medium = Helpful but optional (tests, qa, performance)
🟢 Low = Manual invocation (docs, git, dependencies)
```

### When Suggestions Appear

**Auto-suggest** when:
- ✅ Keywords match agent triggers
- ✅ File patterns match (e.g., editing auth files)
- ✅ Confidence threshold met
- ✅ Context indicates implementation work

**No suggestion** when:
- ❌ Simple information query
- ❌ Already using an agent
- ❌ Low confidence match
- ❌ User explicitly working without agents

---

## Troubleshooting

### "No agents suggested when I expected one"

**Check**:
1. Confidence threshold too high → Lower in `agent-rules.json`
2. Keywords not matching → Add keywords to triggers
3. Wrong file context → Ensure relevant files are open

**Fix**:
```bash
# Lower threshold example
# Edit .claude/agent-rules.json
{
  "name": "backend-architect",
  "confidence_threshold": 0.70  // Was 0.75
}
```

### "Too many suggestions"

**Check**:
1. Confidence threshold too low → Increase in `agent-rules.json`
2. Too many keywords matching → Refine keyword list

**Fix**:
```bash
# Raise threshold example
{
  "name": "agent-name",
  "confidence_threshold": 0.85  // Was 0.75
}
```

### "Pre-commit validation not running"

**Check**:
1. Hook file exists: `.claude/hooks/pre-commit-validation.md`
2. Hook metadata correct (must have `hook: Stop` and `pattern: "git commit"`)
3. Git hooks installed

**Fix**:
```bash
# Verify hook file
cat .claude/hooks/pre-commit-validation.md | head -n 10

# Expected output should include:
# ---
# hook: Stop
# pattern: "git commit"
# ---
```

### "Telemetry not logging"

**Check**:
1. Telemetry directory exists: `mkdir -p telemetry/{suggestions,invocations,validations,workflows}`
2. Write permissions: `chmod -R u+w telemetry/`
3. Hook file exists: `.claude/hooks/post-agent-execution.md`

**Fix**:
```bash
# Create telemetry directories
mkdir -p telemetry/suggestions/$(date +%Y-%m-%d)
mkdir -p telemetry/invocations/$(date +%Y-%m-%d)
mkdir -p telemetry/validations/$(date +%Y-%m-%d)
mkdir -p telemetry/workflows/$(date +%Y-%m-%d)

# Set permissions
chmod -R u+w telemetry/
```

---

## Pro Tips

### Tip 1: Use Agent Patterns Guide
When unsure which agent to use, check `.claude/AGENT_PATTERNS.md` for the decision tree and workflow patterns.

### Tip 2: Let Auto-Activation Learn
Accept/reject suggestions honestly. The system learns from your patterns and improves over time (via weekly auto-adjustment).

### Tip 3: Start with High Priority Agents
Focus on getting these right first:
- debug-specialist
- security-auditor
- design-simplicity-advisor
- code-reviewer
- backend-architect / frontend-developer

### Tip 4: Use Workflow Patterns
For complex tasks, follow proven patterns in `.claude/AGENT_PATTERNS.md`:
- New Feature → Design → Implement → Review → Commit
- Bug Fix → Debug → Fix → Test → Commit
- Security Feature → Security Review → Design → Implement → Security Audit → Commit

### Tip 5: Monitor Telemetry
After 7 days, run analytics to see patterns:
```bash
# Check suggestion acceptance
python scripts/analytics/suggestion_acceptance_rate.py --days=7

# Check agent performance
python scripts/analytics/agent_performance.py --days=7
```

### Tip 6: Progressive Disclosure
For large agents (>500 lines), consider splitting into main + resources:
- Main: Core patterns and common use cases (<500 lines)
- Resources: Deep-dive topics loaded on-demand

---

## Next Steps

### Week 1: Validation Phase
- [ ] Test auto-activation with 10+ different requests
- [ ] Verify pre-commit validation works
- [ ] Check telemetry logging is working
- [ ] Note any false positives/negatives

### Week 2-4: Data Collection
- [ ] Use system normally for 2-3 weeks
- [ ] Let telemetry collect usage data
- [ ] Track suggestion acceptance patterns
- [ ] Identify any issues or needed adjustments

### Month 2: Optimization
- [ ] Run analytics scripts
- [ ] Review suggestion acceptance rates
- [ ] Adjust confidence thresholds if needed
- [ ] Consider progressive disclosure for large agents

### Month 3+: Continuous Improvement
- [ ] Set up automated threshold adjustment (cron job)
- [ ] Monitor metrics monthly
- [ ] Apply progressive disclosure to more agents
- [ ] Share learnings with team

---

## Resources

**Quick Reference**:
- Agent patterns and decision trees → `.claude/AGENT_PATTERNS.md`
- Telemetry integration guide → `.claude/TELEMETRY_INTEGRATION.md`
- Implementation summary → `.claude/IMPLEMENTATION_SUMMARY.md`
- Agent rules configuration → `.claude/agent-rules.json`

**Hooks**:
- Auto-activation → `.claude/hooks/agent-activation-prompt.md`
- Post-execution tracking → `.claude/hooks/post-agent-execution.md`
- Pre-commit validation → `.claude/hooks/pre-commit-validation.md`

**External**:
- Reddit post inspiration: https://www.reddit.com/r/ClaudeAI/comments/1oivjvm/
- Reference implementation: https://github.com/diet103/claude-code-infrastructure-showcase

---

## Support

**Questions?** Check these first:
1. `.claude/AGENT_PATTERNS.md` - Agent selection guide
2. `.claude/IMPLEMENTATION_SUMMARY.md` - Complete feature overview
3. `.claude/TELEMETRY_INTEGRATION.md` - Analytics and learning

**Still stuck?**
- Check telemetry logs for clues
- Review agent-rules.json configuration
- Verify hook files are present and correct
- Test with simple examples first

---

**Status**: ✅ Ready to Use
**Last Updated**: 2025-10-30
**Version**: 1.0.0

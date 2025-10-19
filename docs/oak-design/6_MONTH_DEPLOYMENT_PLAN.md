# 6-Month OaK Deployment Plan

**Automated Rollout for Phases 4-6 with SOPs**

This document provides a complete, automated deployment plan for the OaK architecture over 6 months. Follow this guide step-by-step for systematic implementation.

---

## 📅 Timeline Overview

| Month | Phase | Focus | Automation Level |
|-------|-------|-------|------------------|
| **1** | Phase 4 Start | Transition models + baseline data collection | 80% automated |
| **2** | Phase 4 Complete | Utility tracking + performance dashboards | 90% automated |
| **3** | Phase 5 Start | Agent curation + improvement workflows | 70% automated |
| **4** | Phase 5 Complete | A/B testing + systematic optimization | 75% automated |
| **5** | Phase 6 Start | ML pipeline + data preprocessing | 60% automated |
| **6** | Phase 6 Complete | Policy learning + continuous improvement | 85% automated |

---

## 🚀 Day 1: Immediate Setup (30 minutes)

### Step 1: Add Environment Variables

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Claude OaK Agents Configuration
export OAK_TELEMETRY_ENABLED=true
export OAK_TELEMETRY_DIR="$HOME/Projects/claude-oak-agents/telemetry"
export OAK_PROMPT_FEEDBACK=false
export PYTHONPATH="$HOME/Projects/claude-oak-agents:$PYTHONPATH"

# Phase 4+ Configuration
export OAK_MODELS_DIR="$HOME/Projects/claude-oak-agents/models"
export OAK_ML_DIR="$HOME/Projects/claude-oak-agents/docs/experimental/phase6/ml-pipeline"
```

Then reload:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### Step 2: Verify Hook Installation

```bash
cd ~/Projects/claude-oak-agents

# Check hooks
ls -la ~/.claude/hooks/
# Should show: pre_agent.sh -> .../pre_agent_hook.py
#              post_agent.sh -> .../post_agent_hook.py

# Test end-to-end
python scripts/test_telemetry_e2e.py
```

Expected output: All tests pass with green checkmarks ✅

### Step 3: Schedule Automation Scripts

Add to crontab (`crontab -e`):

```bash
# Weekly telemetry review (every Monday at 9am)
0 9 * * 1 cd $HOME/Projects/claude-oak-agents && python scripts/automation/weekly_review.py >> logs/weekly_review.log 2>&1

# Monthly performance analysis (1st of month at 10am)
0 10 1 * * cd $HOME/Projects/claude-oak-agents && python scripts/automation/monthly_analysis.py >> logs/monthly_analysis.log 2>&1

# Daily health check (every day at 8am)
0 8 * * * cd $HOME/Projects/claude-oak-agents && python scripts/automation/health_check.py >> logs/health_check.log 2>&1
```

### Step 4: Create Log Directory

```bash
mkdir -p ~/Projects/claude-oak-agents/logs
mkdir -p ~/Projects/claude-oak-agents/reports
mkdir -p ~/Projects/claude-oak-agents/backups
```

**✅ Day 1 Complete:** Hooks installed, automation scheduled, ready to collect data!

---

## 📊 Month 1: Phase 4 - Transition Models & Baseline Data

**Goal:** Establish baseline performance metrics and document expected agent behavior.

### Week 1: Baseline Data Collection

**Automated Tasks:**
- ✅ Hooks log all agent invocations automatically
- ✅ Daily health check runs at 8am
- ⚙️ Use agents normally (no changes needed)

**Manual Tasks (5 minutes/day):**
1. **Review daily health check:**
   ```bash
   cat logs/health_check.log
   ```

2. **Spot-check telemetry data:**
   ```bash
   tail -5 telemetry/agent_invocations.jsonl | jq
   ```

**Expected Output:** 50-100 invocations logged by end of week.

### Week 2: Create Transition Models

**Automated Script:**
```bash
python scripts/phase4/generate_transition_models.py
```

**What it does:**
1. Analyzes last week's telemetry data
2. Calculates average duration per agent
3. Determines success rates
4. Identifies common failure patterns
5. Generates `models/transition_expectations.yaml`

**Manual Review (30 minutes):**

Run the review checklist:
```bash
python scripts/phase4/review_transition_models.py
```

This will prompt you to:
- Verify expected durations are reasonable
- Confirm success rates match your experience
- Add preconditions for each agent
- Add postconditions for each agent

**Input Format:**
```
Agent: frontend-developer
Expected duration: 5-30 minutes (calculated)
Success rate: 0.85 (calculated)

Add preconditions (comma-separated, or press Enter to skip):
> UI/UX work required, React/Vue/Angular codebase

Add postconditions (comma-separated, or press Enter to skip):
> Component files created, Styles updated, Tests passing

Save? (y/n): y
```

**Output:** `models/transition_expectations.yaml` with all 29 agents documented.

### Week 3: Utility Tracking Setup

**Automated Script:**
```bash
python scripts/phase4/setup_utility_tracking.py
```

**What it does:**
1. Creates `models/agent_utility_scores.yaml`
2. Initializes all agents with baseline scores
3. Sets up rating prompts

**Enable Feedback Prompts (Optional):**
```bash
export OAK_PROMPT_FEEDBACK=true
```

When enabled, after each agent execution:
```
📊 Quick feedback for backend-architect:
  Success? (y/n): y
  Quality (1-5): 4
  Would use again? (y/n): y
  Notes (optional): Great API design
  ✓ Feedback recorded!
```

**Or batch feedback (recommended):**
```bash
python scripts/phase4/batch_feedback.py --last-week
```

This shows all agents from last week and lets you rate them in bulk.

### Week 4: Performance Dashboard

**Automated Script:**
```bash
python scripts/phase4/generate_dashboard.py
```

**What it does:**
1. Reads all telemetry data
2. Generates HTML dashboard with charts
3. Saves to `reports/dashboard_YYYY-MM-DD.html`

**Review Dashboard (10 minutes/week):**
```bash
open reports/dashboard_$(date +%Y-%m-%d).html
```

Dashboard shows:
- Agent usage frequency (bar chart)
- Success rates over time (line chart)
- Average quality scores (radar chart)
- Top performers and underperformers
- Recommended actions

**End of Month 1 Checklist:**
```bash
python scripts/phase4/month1_checklist.py
```

Expected output:
- ✅ 200+ invocations logged
- ✅ All agents have transition models
- ✅ Utility scores initialized
- ✅ First dashboard generated

---

## 🔄 Month 2: Phase 4 Complete - Optimization & Refinement

**Goal:** Refine transition models based on data and establish review cadence.

### Week 5-6: Model Refinement

**Automated Analysis:**
```bash
python scripts/phase4/analyze_deviations.py
```

This compares actual vs expected behavior and flags anomalies:
```
🔍 Deviation Analysis:

Agent: backend-architect
  Expected duration: 10-45 min
  Actual average: 62 min ⚠️  OUTLIER
  Recommendation: Investigate why tasks taking longer

Agent: frontend-developer
  Expected success rate: 0.85
  Actual success rate: 0.92 ✓ EXCEEDING
  Recommendation: Consider for complex tasks

Total anomalies found: 3
See reports/deviations_YYYY-MM-DD.md for details
```

**Manual Review (1 hour):**

Open deviation report:
```bash
cat reports/deviations_$(date +%Y-%m-%d).md
```

For each anomaly:
1. Review telemetry logs for that agent
2. Determine if expectation needs adjustment
3. Update transition model if needed

**Update transition models:**
```bash
python scripts/phase4/update_transition_model.py <agent_name>
```

Interactive prompts guide you through updates.

### Week 7-8: Utility Score Calibration

**Automated Recommendations:**
```bash
python scripts/phase4/recommend_utility_updates.py
```

Analyzes recent performance and suggests utility score changes:
```
📊 Utility Score Recommendations:

frontend-developer:
  Current: 0.85
  Recommended: 0.90 (+0.05)
  Reason: 95% success rate, 4.2/5 avg quality
  Apply? (y/n): y

debug-specialist:
  Current: 0.80
  Recommended: 0.75 (-0.05)
  Reason: 70% success rate on complex issues
  Apply? (y/n): y

Applied 2 updates to models/agent_utility_scores.yaml
```

**End of Month 2 Checklist:**
```bash
python scripts/phase4/month2_checklist.py
```

Expected output:
- ✅ 400+ invocations logged
- ✅ Transition models calibrated
- ✅ Utility scores reflect reality
- ✅ Weekly review cadence established

---

## 🎯 Month 3: Phase 5 - Adaptive Curation Begins

**Goal:** Use telemetry data to systematically improve agent performance.

### Week 9: Agent Performance Audit

**Automated Analysis:**
```bash
python scripts/phase5/audit_agents.py
```

Generates comprehensive agent report:
```
📊 Agent Performance Audit - 2025-01-15

HIGH PERFORMERS (>0.85 success, >4.0 quality):
  ✓ frontend-developer: 0.92 success, 4.3 quality, 45 uses
  ✓ unit-test-expert: 0.88 success, 4.5 quality, 32 uses

NEEDS IMPROVEMENT (<0.70 success OR <3.5 quality):
  ⚠️  backend-architect: 0.68 success, 3.2 quality, 28 uses
      - Failure pattern: API design inconsistencies
      - Recommendation: Refine API design guidelines

  ⚠️  debug-specialist: 0.65 success, 3.8 quality, 15 uses
      - Failure pattern: Complex multi-layer issues
      - Recommendation: Add systematic debugging workflow

UNDERUTILIZED (<5 uses despite high scores):
  📉 blockchain-developer: 0.90 success, 4.0 quality, 3 uses
  📉 ml-engineer: 0.85 success, 4.2 quality, 4 uses

OVERUTILIZED (Could delegate to specialists):
  📈 general-purpose: 18 uses (should use specialized agents)

See reports/agent_audit_YYYY-MM-DD.md for full details
```

**Manual Review (2 hours):**

Open audit report and prioritize improvements:
```bash
cat reports/agent_audit_$(date +%Y-%m-%d).md
```

Select 2-3 agents for improvement this month.

### Week 10: Agent Improvement Workflow

For each selected agent:

**Step 1: Analyze Failures**
```bash
python scripts/phase5/analyze_failures.py <agent_name>
```

Shows all failed invocations with context:
```
Failure Analysis: backend-architect

Invocation #1 (2025-01-10):
  Task: Design REST API for auth service
  Duration: 75 minutes
  Outcome: partial
  Issue: Inconsistent naming conventions
  Files modified: [api/auth.ts, api/users.ts]

Common patterns across failures:
  - Naming convention inconsistencies (5 occurrences)
  - Missing error handling patterns (3 occurrences)
  - Incomplete OpenAPI specs (4 occurrences)

Recommended improvements:
  1. Add naming convention guidelines to agent prompt
  2. Include error handling checklist
  3. Require OpenAPI spec validation
```

**Step 2: Generate Improvement Proposal**
```bash
python scripts/phase5/propose_improvement.py <agent_name>
```

Creates improvement proposal in `reports/improvements/<agent_name>_proposal.md`:
```markdown
# Improvement Proposal: backend-architect

## Current Issues
- Naming convention inconsistencies
- Missing error handling patterns
- Incomplete OpenAPI specs

## Proposed Changes

### 1. Enhanced Prompt Additions
Add to agent markdown:
```
## API Design Guidelines
- Use camelCase for JSON fields
- Include error codes: 4xx (client), 5xx (server)
- Generate OpenAPI 3.0 spec for all endpoints
```

### 2. Quality Checklist
Before completion, verify:
- [ ] Naming conventions consistent
- [ ] All endpoints have error handling
- [ ] OpenAPI spec validates
```

**Step 3: Apply Improvements**
```bash
python scripts/phase5/apply_improvement.py <agent_name>
```

This:
1. Backs up current agent file
2. Applies proposed changes
3. Creates A/B test configuration
4. Schedules comparison period

### Week 11-12: A/B Testing

**Automated A/B Test:**
```bash
# Test runs automatically via hooks
# Check status:
python scripts/phase5/ab_test_status.py
```

Shows current tests:
```
Active A/B Tests:

backend-architect (improved vs original):
  Test period: 2025-01-15 to 2025-02-15
  Current stats (Day 14):
    Improved version: 12 uses, 0.83 success, 4.1 quality
    Original version: 11 uses, 0.68 success, 3.2 quality
  Status: Improved version winning ✓

  Auto-promote in 16 days or run:
    python scripts/phase5/promote_agent.py backend-architect
```

**Manual Review (weekly 15 minutes):**
```bash
python scripts/phase5/review_ab_tests.py
```

Prompts you to:
- Review ongoing tests
- Promote winners early (if clear)
- Extend tests if inconclusive
- Rollback if new version worse

**End of Month 3 Checklist:**
```bash
python scripts/phase5/month3_checklist.py
```

Expected output:
- ✅ 600+ invocations logged
- ✅ Agent audit completed
- ✅ 2-3 agents improved
- ✅ A/B testing active

---

## 🔧 Month 4: Phase 5 Complete - Systematic Curation

**Goal:** Establish continuous improvement process.

### Week 13-14: Curation Automation

**Setup Monthly Curation Workflow:**
```bash
python scripts/phase5/setup_curation_workflow.py
```

This creates automated monthly workflow:
1. Agent audit runs automatically
2. Top 3 improvement candidates identified
3. Improvement proposals generated
4. Email/Slack notification sent

**Curation Meeting (monthly, 1 hour):**

Agenda auto-generated:
```bash
python scripts/phase5/generate_curation_agenda.py
```

Output in `reports/curation/agenda_YYYY-MM.md`:
```markdown
# Agent Curation Meeting - February 2025

## Agenda

1. Review Month Performance (5 min)
   - 200 total invocations
   - 3 agents improved last month
   - Overall success rate: 0.82 (up from 0.78)

2. Active A/B Tests (10 min)
   - backend-architect: Promote improved version
   - debug-specialist: Extend test 2 weeks

3. New Improvement Candidates (20 min)
   - security-auditor: 0.65 success rate
   - qa-specialist: Taking 2x expected time
   - infrastructure-specialist: Missing CDK best practices

4. Prioritization (15 min)
   Select 2-3 for next month

5. Gap Analysis (10 min)
   - New agents needed?
   - Overlapping responsibilities?
   - Underutilized agents to deprecate?
```

**Decision Recording:**
```bash
python scripts/phase5/record_curation_decisions.py
```

Interactive prompts record:
- Which agents to improve
- A/B test decisions
- New agent proposals
- Deprecation candidates

### Week 15-16: Agent Lifecycle Management

**Automated Deprecation Analysis:**
```bash
python scripts/phase5/analyze_deprecation_candidates.py
```

Identifies agents for potential retirement:
```
Deprecation Candidates:

general-purpose:
  Usage: 0 invocations in 60 days
  Reason: Restricted agent, users prefer specialists
  Recommendation: Archive (keep for emergencies)

legacy-maintainer:
  Usage: 1 invocation in 90 days
  Reason: No legacy projects active
  Recommendation: Deprecate temporarily

blockchain-developer:
  Usage: 3 invocations in 60 days
  Reason: No active blockchain projects
  Recommendation: Keep but optimize for future use
```

**New Agent Proposals:**
```bash
python scripts/phase5/analyze_gaps.py
```

Identifies missing specializations:
```
Agent Gap Analysis:

Potential New Agents:

1. api-security-specialist
   Evidence: 15 security-auditor invocations focused on API security
   Recommendation: Specialize from security-auditor
   Priority: High

2. database-architect
   Evidence: backend-architect spending 40% time on database design
   Recommendation: Split backend-architect responsibilities
   Priority: Medium

3. cloud-cost-optimizer
   Evidence: infrastructure-specialist invocations mention cost 8 times
   Recommendation: New specialization
   Priority: Low
```

**Create New Agent (when approved):**
```bash
python scripts/phase5/create_new_agent.py <agent-name>
```

Guides you through:
- Agent purpose and scope
- Tool access requirements
- Integration with existing agents
- Initial transition model

**End of Month 4 Checklist:**
```bash
python scripts/phase5/month4_checklist.py
```

Expected output:
- ✅ 800+ invocations logged
- ✅ Monthly curation workflow established
- ✅ 5+ agents improved total
- ✅ Agent lifecycle managed

---

## 🤖 Month 5: Phase 6 - ML Pipeline Setup

**Goal:** Begin offline reinforcement learning for agent selection.

### Week 17-18: Data Preparation

**Automated Data Preprocessing:**
```bash
python scripts/phase6/prepare_training_data.py
```

What it does:
1. Loads all telemetry data (8+ weeks)
2. Cleans and normalizes records
3. Engineers features for ML
4. Splits into train/validation/test sets
5. Exports to `ml-pipeline/data/`

**Quality Check:**
```bash
python scripts/phase6/validate_training_data.py
```

Shows data quality report:
```
Training Data Quality Report:

Total Records: 876
Train: 613 (70%)
Validation: 175 (20%)
Test: 88 (10%)

Feature Coverage:
  ✓ Codebase features: 100%
  ✓ Task features: 100%
  ✓ Context features: 95% (missing tests_passing for 5%)
  ⚠️  Historical features: 60% (early data lacks history)

Label Distribution:
  Success: 720 (82%)
  Partial: 98 (11%)
  Failure: 58 (7%)

Data Quality: GOOD ✓
Ready for training: YES
```

### Week 19: Baseline Model Training

**Train Baseline Models:**
```bash
python scripts/phase6/train_baseline_models.py
```

Trains multiple baseline models:
- Random Forest (agent selection)
- Logistic Regression (success prediction)
- Neural Network (quality prediction)

Output:
```
Training Baseline Models...

1. Random Forest (Agent Selection):
   Training accuracy: 0.85
   Validation accuracy: 0.78
   Test accuracy: 0.76
   ✓ Saved to ml-pipeline/models/rf_agent_selection.pkl

2. Logistic Regression (Success Prediction):
   Training accuracy: 0.82
   Validation accuracy: 0.80
   Test accuracy: 0.79
   ✓ Saved to ml-pipeline/models/lr_success_prediction.pkl

3. Neural Network (Quality Prediction):
   Training MAE: 0.45
   Validation MAE: 0.52
   Test MAE: 0.51
   ✓ Saved to ml-pipeline/models/nn_quality_prediction.pt

Baseline models ready!
Next: Train RL policy with: python scripts/phase6/train_rl_policy.py
```

### Week 20: Offline RL Training

**Train RL Policy:**
```bash
python scripts/phase6/train_rl_policy.py --config docs/experimental/phase6/rl_config.yaml
```

Uses offline RL (Conservative Q-Learning) to learn agent selection policy.

Configuration in `docs/experimental/phase6/rl_config.yaml`:
```yaml
rl_training:
  algorithm: CQL  # Conservative Q-Learning
  episodes: 1000
  batch_size: 64
  learning_rate: 0.0003
  discount_factor: 0.99

  state_features:
    - risk_level
    - scope
    - complexity
    - tests_passing
    - historical_success_rate

  action_space:
    - agent_selection (29 agents)

  reward_function:
    success: +10
    partial: +5
    failure: -10
    quality_bonus: quality_rating * 2
    duration_penalty: -duration_seconds / 60
```

Training output:
```
Training Offline RL Policy...

Episode 100/1000: Avg Reward: 5.2, Loss: 0.45
Episode 200/1000: Avg Reward: 6.8, Loss: 0.32
Episode 300/1000: Avg Reward: 7.5, Loss: 0.28
...
Episode 1000/1000: Avg Reward: 9.2, Loss: 0.15

Training complete!
Final evaluation on test set:
  - Average reward: 8.7
  - Agent selection accuracy: 0.82
  - Better than random baseline: +32%
  - Better than heuristic baseline: +12%

Model saved to: ml-pipeline/models/rl_policy_v1.pt
```

**End of Month 5 Checklist:**
```bash
python scripts/phase6/month5_checklist.py
```

Expected output:
- ✅ 1000+ invocations logged
- ✅ Training data prepared
- ✅ Baseline models trained
- ✅ RL policy trained (v1)

---

## 🚀 Month 6: Phase 6 Complete - Deployment & Continuous Learning

**Goal:** Deploy ML-based agent selection and establish continuous learning loop.

### Week 21-22: Policy Deployment

**Export Policy to Production:**
```bash
python scripts/phase6/export_policy.py --model ml-pipeline/models/rl_policy_v1.pt
```

Exports policy to YAML rules:
```yaml
# models/learned_policy_v1.yaml
policy_version: 1
created_at: 2025-03-01
algorithm: CQL

agent_selection_rules:
  high_risk_feature_development:
    conditions:
      risk_level: [high, critical]
      task_type: feature_development
    recommended_agents:
      - name: security-auditor
        confidence: 0.92
      - name: systems-architect
        confidence: 0.87
    expected_reward: 8.5

  broken_tests:
    conditions:
      tests_passing: false
    recommended_agents:
      - name: debug-specialist
        confidence: 0.95
      - name: unit-test-expert
        confidence: 0.78
    expected_reward: 7.8

  # ... more rules
```

**Create Policy-Advisor Agent:**
```bash
python scripts/phase6/create_policy_advisor_agent.py
```

Generates new agent: `agents/policy-advisor.md`

This agent:
- Reads learned policy YAML
- Recommends agents based on ML model
- Provides confidence scores
- Falls back to heuristics if needed

**Deploy to Production:**
```bash
# Backup current agents
python scripts/phase6/backup_current_config.py

# Deploy policy advisor
cp agents/policy-advisor.md ~/.claude/agents/

# Update project-manager to use policy advisor
python scripts/phase6/update_project_manager.py
```

### Week 23: Validation & Monitoring

**Shadow Mode Validation:**
```bash
export OAK_POLICY_MODE=shadow  # Recommend but don't enforce
```

In shadow mode:
- Policy advisor makes recommendations
- User can override
- Both choices logged for comparison

**Monitor Performance:**
```bash
python scripts/phase6/monitor_policy_performance.py
```

Shows real-time comparison:
```
Policy Performance Monitoring:

Last 7 days:
  ML Policy recommendations: 45 invocations
    - Followed: 38 (84%)
    - Overridden: 7 (16%)

  When followed:
    - Success rate: 0.87
    - Avg quality: 4.3

  When overridden:
    - Success rate: 0.71
    - Avg quality: 3.8

  Conclusion: ML policy performing BETTER than manual selection
  Recommendation: Enable enforcement mode

Override reasons (when user chose different agent):
  1. "Wanted faster completion" (3 times)
  2. "Preferred familiar agent" (2 times)
  3. "ML suggested agent unavailable" (2 times)
```

### Week 24: Continuous Learning Setup

**Enable Active Policy Updates:**
```bash
export OAK_POLICY_MODE=active  # Enforce recommendations
export OAK_POLICY_RETRAINING=weekly  # Retrain every week
```

**Automated Retraining Pipeline:**
```bash
# Add to crontab
0 2 * * 0 cd $HOME/Projects/claude-oak-agents && python scripts/phase6/retrain_policy.py >> logs/retraining.log 2>&1
```

Retraining script:
1. Collects new telemetry from last week
2. Adds to training dataset
3. Retrains policy with updated data
4. Validates on held-out test set
5. Auto-deploys if improvement > 2%
6. Otherwise keeps current policy

**Performance Dashboard:**
```bash
python scripts/phase6/generate_ml_dashboard.py
```

Shows:
- Policy performance over time
- Feature importance
- Agent selection distribution
- Reward trends
- Continuous improvement metrics

**End of Month 6 Checklist:**
```bash
python scripts/phase6/month6_checklist.py
```

Expected output:
- ✅ 1200+ invocations logged
- ✅ ML policy deployed
- ✅ Continuous learning active
- ✅ System fully automated!

---

## 📋 Maintenance SOPs

### Daily Tasks (Automated)

**Health Check (8am daily)**
```bash
# Runs automatically via cron
# Check results:
cat logs/health_check.log
```

What it checks:
- Telemetry files writable
- Hooks functioning
- No disk space issues
- Recent invocations logged

**Expected:** No errors, green status

---

### Weekly Tasks (30 minutes)

**Monday Morning Review:**

1. **Check Weekly Report:**
   ```bash
   cat reports/weekly_report_$(date +%Y-%m-%d).html
   ```

   Review:
   - Total invocations this week
   - Agent success rates
   - Any anomalies flagged

2. **Review Active A/B Tests:**
   ```bash
   python scripts/phase5/review_ab_tests.py
   ```

   Action: Promote/extend/rollback as needed

3. **Check Policy Performance (Phase 6+):**
   ```bash
   python scripts/phase6/monitor_policy_performance.py
   ```

   Action: Note any degradation

**Time Required:** 15-30 minutes

---

### Monthly Tasks (2 hours)

**First Monday of Month:**

1. **Run Monthly Analysis:**
   ```bash
   python scripts/automation/monthly_analysis.py
   ```

   Generates comprehensive report in `reports/monthly/YYYY-MM.html`

2. **Curation Meeting:**
   ```bash
   python scripts/phase5/generate_curation_agenda.py
   cat reports/curation/agenda_YYYY-MM.md
   ```

   Review and make decisions:
   - Agents to improve
   - A/B test results
   - New agent proposals
   - Deprecation candidates

3. **Record Decisions:**
   ```bash
   python scripts/phase5/record_curation_decisions.py
   ```

   Interactive prompts guide you through recording all decisions.

4. **Approve Improvements:**
   ```bash
   python scripts/phase5/apply_approved_improvements.py
   ```

   Implements decisions from curation meeting.

**Time Required:** 1-2 hours

---

### Quarterly Tasks (4 hours)

**First Week of Quarter:**

1. **Comprehensive Audit:**
   ```bash
   # Future: python scripts/audit/quarterly_audit.py (to be implemented)
   ```

   Full system analysis:
   - All agent performance metrics
   - Telemetry data quality
   - ML model performance
   - Infrastructure health

2. **Strategic Review:**
   - OaK architecture effectiveness
   - Business value delivered
   - System ROI analysis
   - Roadmap for next quarter

3. **System Optimization:**
   ```bash
   # Future: python scripts/maintenance/optimize_system.py (to be implemented)
   ```

   - Archive old telemetry data (manual for now)
   - Optimize database queries (manual for now)
   - Update dependencies (manual for now)
   - Security updates (manual for now)

4. **Team Sync:**
   - Share quarterly report with team
   - Gather feedback on agent system
   - Identify new use cases
   - Plan agent expansions

**Time Required:** 3-4 hours

---

## 📊 Input/Output Reference Guide

### Telemetry Data Inputs

**Agent Invocation Data (Automatic via Hooks):**
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "agent_name": "backend-architect",
  "task_description": "Design REST API for auth service",
  "state_features": {
    "codebase": {...},
    "task": {...},
    "context": {...}
  },
  "duration_seconds": 1800,
  "outcome": "success",
  "files_modified": [...]
}
```

**Success Metrics (Manual or Automated):**
```json
{
  "invocation_id": "uuid",
  "success": true,
  "quality_rating": 4,
  "feedback_source": "human",
  "feedback_notes": "Good API design, minor improvements needed"
}
```

### How to Provide Feedback

**Method 1: Interactive Prompts**
```bash
export OAK_PROMPT_FEEDBACK=true
# After each agent execution, you'll be prompted
```

**Method 2: Batch Feedback (Recommended)**
```bash
python scripts/phase4/batch_feedback.py --last-week
```

Shows list of agents, you rate each:
```
Agent 1/15: backend-architect (2025-01-15)
Task: Design REST API for auth service
Duration: 30 minutes
Outcome: success

Success? (y/n): y
Quality (1-5): 4
Notes: Good structure, missing error codes
[Enter to continue]
```

**Method 3: Feedback File**

Create `feedback.yaml`:
```yaml
- invocation_id: "uuid-here"
  success: true
  quality_rating: 4
  notes: "Great work"

- invocation_id: "uuid-here2"
  success: false
  quality_rating: 2
  notes: "Missed requirements"
```

Import:
```bash
python scripts/phase4/import_feedback.py feedback.yaml
```

### Expected Outputs

**Weekly Report:**
```
📊 Weekly Report: Jan 15-22, 2025

Total Invocations: 42
Success Rate: 83% (↑ 5% from last week)
Average Quality: 4.1/5.0

Top Performers:
  1. frontend-developer: 12 uses, 92% success
  2. unit-test-expert: 8 uses, 88% success

Needs Attention:
  - debug-specialist: 65% success (below 75% threshold)

Recommendations:
  - Review debug-specialist failures
  - Continue current practices for top performers
```

**Monthly Dashboard:**

HTML file with:
- Agent usage treemap
- Success rate trends (line chart)
- Quality distribution (box plot)
- Duration analysis
- Actionable recommendations

**ML Policy Recommendations:**
```yaml
task: "Implement OAuth2 authentication"
state:
  risk_level: high
  scope: large

ml_recommendation:
  primary_agents:
    - name: security-auditor
      confidence: 0.92
      expected_success_rate: 0.85
      expected_duration: 45min

    - name: backend-architect
      confidence: 0.87
      expected_success_rate: 0.82
      expected_duration: 120min

  reasoning: "High risk + large scope historically succeed with security-first approach"
```

---

## 🚨 Troubleshooting

### Issue: Hooks Not Logging

**Check:**
```bash
ls -la ~/.claude/hooks/
echo $OAK_TELEMETRY_ENABLED
cat logs/health_check.log
```

**Fix:**
```bash
./hooks/install_hooks.sh
export OAK_TELEMETRY_ENABLED=true
```

### Issue: Training Data Insufficient

**Check:**
```bash
wc -l telemetry/agent_invocations.jsonl
```

**Need:** Minimum 200 invocations for Phase 6

**Fix:** Wait and accumulate more data, or:
```bash
python scripts/phase6/generate_synthetic_data.py --augment
```

### Issue: ML Model Performance Degrading

**Check:**
```bash
python scripts/phase6/monitor_policy_performance.py
```

**Fix:**
```bash
python scripts/phase6/retrain_policy.py --force
python scripts/phase6/validate_new_policy.py
```

### Issue: Automation Script Failed

**Check:**
```bash
tail -50 logs/<script_name>.log
```

**Fix:** Usually permissions or environment variables

---

## 📈 Success Metrics

Track these over 6 months:

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Total Invocations | 200 | 600 | 1200 |
| Overall Success Rate | 75% | 80% | 85% |
| Average Quality | 3.5 | 4.0 | 4.3 |
| Agents Improved | 0 | 5 | 12 |
| Time Saved (hrs/week) | 0 | 2 | 5 |
| Manual Review Time (min/week) | 60 | 30 | 15 |

---

## 🎯 Summary

**Automation Levels:**
- **Phase 1-2:** 95% automated (hooks log everything)
- **Phase 4:** 80% automated (weekly review + monthly curation)
- **Phase 5:** 70% automated (improvement proposals, A/B testing)
- **Phase 6:** 85% automated (continuous learning, auto-deployment)

**Time Investment:**
- **Setup:** 30 minutes (Day 1)
- **Daily:** 0 minutes (fully automated)
- **Weekly:** 15-30 minutes (review reports)
- **Monthly:** 1-2 hours (curation meeting)
- **Quarterly:** 3-4 hours (strategic review)

**By Month 6:** Fully automated agent selection with continuous improvement, minimal manual intervention required!

---

**Next:** Begin Day 1 setup above ↑

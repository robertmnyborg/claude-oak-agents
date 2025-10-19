# OaK Agents - Quick Start Guide

**Get started with the OaK architecture in 5 minutes**

---

## ✅ Setup (Complete Today)

### 1. Install Telemetry Hooks

Install automatic telemetry logging:

```bash
cd ~/Projects/claude-oak-agents
./hooks/install_hooks.sh
```

This installs:
- ✅ **Pre-agent hook**: Logs agent invocation start with state features
- ✅ **Post-agent hook**: Logs completion with duration and outcome
- ✅ **Environment variables**: Adds to `~/.zshrc` automatically
- ✅ **Fail-safe design**: Hooks never block agent execution

**What gets logged**:
- Agent name, type, task description
- State features (languages, frameworks, LOC, complexity)
- Execution metrics (duration, success/failure, files modified)
- All data stored locally in `telemetry/` directory

### 2. Verify Installation

```bash
cd ~/Projects/claude-oak-agents

# Check hooks are installed
ls -la ~/.claude/hooks/

# Verify environment variables (in new terminal)
echo $OAK_TELEMETRY_ENABLED  # Should show: true

# Test the system (optional)
python scripts/test_telemetry_e2e.py
```

Expected: All green checkmarks ✅

### 3. Install Automation (Recommended)

Set up automated prompts and scheduled reviews:

```bash
cd ~/Projects/claude-oak-agents
./automation/install_automation.sh
```

This installs:
- ✅ Shell prompts (reminds you when reviews are due)
- ✅ Scheduled execution (runs reviews automatically)
- ✅ Notifications (alerts when results are ready)

**Alternative:** Skip automation and run reviews manually (see sections below)

### 4. Start Using It

That's it! The system is ready:
- Hooks log automatically when agents run
- Automation prompts you when reviews are due
- Just use agents normally in Claude Code

---

## 📅 6-Month Roadmap

Full details in: [`docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md`](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)

**Month 1-2: Phase 4** - Transition models & utility tracking
**Month 3-4: Phase 5** - Agent curation & A/B testing
**Month 5-6: Phase 6** - ML pipeline & continuous learning

---

## 📊 Weekly Routine (15 minutes)

**Automated:** System runs every Monday at 9am and notifies you

**Manual alternative:**
```bash
# Generate weekly report
oak-weekly-review

# Or directly:
python3 scripts/automation/weekly_review.py
open reports/weekly_report_$(date +%Y-%m-%d).html
```

---

## 🔧 Monthly Routine (1 hour)

**Automated:** System runs 1st of month at 10am and notifies you

**Manual alternative:**
```bash
# Generate monthly analysis
oak-monthly-review

# Or directly:
python3 scripts/automation/monthly_analysis.py
cat reports/curation/agenda_$(date +%Y-%m).md

# Make decisions (interactive)
python3 scripts/phase5/record_curation_decisions.py
```

---

## 📈 Check Progress

```bash
# System status (shows last reviews, new invocations)
oak-status

# View performance dashboard
oak-dashboard

# Check system health
oak-health-check

# View raw telemetry
cat telemetry/agent_invocations.jsonl | jq | tail -20

# Analyze performance
python3 telemetry/analyzer.py
```

---

## 🆘 Need Help?

1. **[Automation README](automation/README.md)** - Shell prompts, notifications, scheduling
2. **[6-Month Deployment Plan](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Complete automated roadmap
3. **[Implementation Guide](docs/oak-design/IMPLEMENTATION_GUIDE.md)** - Technical details
4. **[OaK Architecture](docs/oak-design/OAK_ARCHITECTURE.md)** - System design
5. **[Hooks README](hooks/README.md)** - Telemetry hooks documentation

---

**Next:** Follow the 6-Month Deployment Plan for systematic rollout →

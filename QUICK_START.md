# OaK Agents - Quick Start Guide

**Get started with the OaK architecture in 5 minutes**

---

## ✅ Setup (Complete Today)

### 1. Add Environment Variables

Add to `~/.zshrc`:
```bash
export OAK_TELEMETRY_ENABLED=true
export OAK_TELEMETRY_DIR="$HOME/Projects/claude-oak-agents/telemetry"
export OAK_PROMPT_FEEDBACK=false
export PYTHONPATH="$HOME/Projects/claude-oak-agents:$PYTHONPATH"
```

Reload:
```bash
source ~/.zshrc
```

### 2. Verify Installation

```bash
cd ~/Projects/claude-oak-agents

# Hooks should already be installed
ls -la ~/.claude/hooks/

# Test the system
python scripts/test_telemetry_e2e.py
```

Expected: All green checkmarks ✅

### 3. Start Using It

That's it! Hooks are now logging automatically. Use agents normally in Claude Code.

---

## 📅 6-Month Roadmap

Full details in: [`docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md`](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)

**Month 1-2: Phase 4** - Transition models & utility tracking
**Month 3-4: Phase 5** - Agent curation & A/B testing
**Month 5-6: Phase 6** - ML pipeline & continuous learning

---

## 📊 Weekly Routine (15 minutes)

Every Monday:
```bash
# Generate weekly report
python scripts/automation/weekly_review.py

# View report
open reports/weekly_report_$(date +%Y-%m-%d).html
```

---

## 🔧 Monthly Routine (1 hour)

First Monday of month:
```bash
# Generate monthly analysis
python scripts/automation/monthly_analysis.py

# Review curation agenda
cat reports/curation/agenda_$(date +%Y-%m).md

# Make decisions (interactive)
python scripts/phase5/record_curation_decisions.py
```

---

## 📈 Check Progress

```bash
# View telemetry
cat telemetry/agent_invocations.jsonl | jq | tail -20

# Analyze performance
python telemetry/analyzer.py

# View dashboard
python scripts/phase4/generate_dashboard.py
open reports/dashboard_$(date +%Y-%m-%d).html
```

---

## 🆘 Need Help?

1. **[6-Month Deployment Plan](docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md)** - Complete automated roadmap
2. **[Implementation Guide](docs/oak-design/IMPLEMENTATION_GUIDE.md)** - Technical details
3. **[OaK Architecture](docs/oak-design/OAK_ARCHITECTURE.md)** - System design
4. **[Hooks README](hooks/README.md)** - Telemetry hooks documentation

---

**Next:** Follow the 6-Month Deployment Plan for systematic rollout →

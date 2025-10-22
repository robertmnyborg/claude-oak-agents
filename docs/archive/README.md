# Archive Directory

This directory contains historical documentation and files that are no longer actively used but preserved for reference.

## Directory Structure

### `phase2/` - Phase 2 & 2A Implementation Docs
Historical documentation from Phase 2 (Workflow Coordination) and Phase 2A (Minimal Workflow Tracking) implementations.

**Contents**:
- Phase-specific README and quick start guides
- Implementation summaries and integration notes
- Verification scripts

**Status**: Fully integrated into main documentation (CLAUDE.md, README.md, QUICK_START.md)

**Archive Date**: 2025-10-21

---

### `deliverables/` - Project Delivery Documentation
Project milestone tracking and delivery documentation.

**Contents**:
- Project deliverables tracking
- Feature delivery notes (e.g., Compaction feature)

**Status**: Historical project management artifacts

**Archive Date**: 2025-10-21

---

### `claude-squad-legacy/` - Original Squad Commands
Legacy slash commands from the original claude-squad system.

**Contents**:
- `/squad-assemble`, `/squad-deploy`, `/squad-dismiss`
- `/squad-furlough`, `/squad-off`, `/squad-on`
- `/squad-override`, `/squad-standdown`, `/squad-status`

**Status**: OaK system uses different workflow (telemetry-based, `oak-*` commands)

**Archive Date**: 2025-10-21

---

### `agent-reports/` - Agent Creation Reports
Reports generated during agent creation process.

**Contents**:
- Creation reports for agents built by agent-creator
- Analysis and specification documents

**Status**: Historical artifacts from agent creation workflow

**Archive Date**: 2025-10-21

---

### `experimental/compaction/` - Compaction Feature
Experimental context compression utility for agent output reduction.

**Contents**:
- Context compression implementation (compaction.py)
- Unit tests and validation scripts
- Documentation (README, Quick Start, Integration Guide)
- Example workflows

**Status**: Experimental code, no production usage found

**Archive Date**: 2025-10-21

---

### Previous Archives

#### `ANTHROPIC_SKILLS_PARITY.md`
Documentation of parity between Anthropic Skills and Claude OaK Agents.

#### `EXECUTIVE_OVERVIEW.md`
Executive summary comparing claude-oak-agents vs claude-squad.

#### `KISS_ENHANCEMENTS.md`
KISS principle enhancements and simplification documentation.

#### `oak_architecture_lecture.md`
Detailed lecture notes on OaK architecture design.

#### `RELEASE_NOTES_v2.0.0.md`
Release notes for version 2.0.0.

---

## Accessing Archived Files

All files are preserved in git history. To restore a file:

```bash
# View archived file
cat docs/archive/phase2/README_PHASE2.md

# Restore to root (if needed)
cp docs/archive/phase2/README_PHASE2.md ./

# Or restore from git if accidentally deleted
git checkout HEAD -- docs/archive/phase2/README_PHASE2.md
```

---

## Why Files Were Archived

**Rationale**:
- **Phase 2/2A docs**: Features fully integrated into main documentation
- **Delivery docs**: Project milestones completed, historical value only
- **Squad commands**: Legacy system, OaK uses different workflow
- **Agent reports**: Creation artifacts, not runtime documentation

**Principle**: Keep active docs minimal and focused. Archive historical/phase-specific documentation for reference.

---

**Archive Maintained By**: Repository cleanup process
**Last Updated**: 2025-10-21

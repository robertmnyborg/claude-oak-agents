# Repository Cleanup Plan - claude-oak-agents

**Analysis Date**: 2025-10-21
**Analyst**: Design Simplicity Advisor
**Objective**: Remove bloat, consolidate documentation, improve maintainability

---

## Executive Summary

### Findings Overview

- **13 root-level documentation files** (excessive for user experience)
- **1,001-line file in wrong repository** (customer-feature-analysis.md)
- **5 compaction-related files** with no production usage
- **9 legacy squad commands** not referenced in current system
- **2 duplicate UX designer files** (agent + report)
- **Multiple phase-specific docs** duplicating main documentation
- **No critical dependencies** on files marked for deletion

### Impact Assessment

- **Safe Deletions**: 1 file (1,001 lines)
- **Archive Operations**: 14 files (phase-specific docs, reports, legacy commands)
- **Potential Removals**: 5 files (unused compaction feature) - needs confirmation
- **Documentation Consolidation**: 10+ root files → 3-4 canonical files
- **Net Reduction**: ~30-40% reduction in root-level clutter

---

## Category 1: IMMEDIATE DELETION (100% Certain)

### 1.1 Wrong Repository Files

**File**: `customer-feature-analysis.md` (1,001 lines)

**Reasoning**:
- Analysis of "apps-feature-analyst" product features
- References multi-workspace context (`/Users/robertnyborg/Projects/CLAUDE.md`)
- Contains customer conversation transcripts for different product
- Zero references in this repository
- Clearly belongs in `apps-feature-analyst` project

**Action**:
```bash
rm /Users/robertnyborg/Projects/claude-oak-agents/customer-feature-analysis.md
```

**Risk**: ZERO - This file is completely unrelated to claude-oak-agents

---

## Category 2: ARCHIVE (Historical/Phase-Specific)

### 2.1 Phase-Specific Documentation

These documents describe phase-specific implementations that are now integrated into main system.

#### Phase 2 Documentation (4 files)

**Files**:
- `README_PHASE2.md` (Phase 2 overview, duplicates main README sections)
- `QUICK_START_PHASE2.md` (Phase 2 quick start, duplicates main QUICK_START.md)
- `PHASE2_IMPLEMENTATION_SUMMARY.md` (Implementation notes, historical)
- `INTEGRATION_SUMMARY.md` (Phase 2 integration details, historical)

**Reasoning**:
- Phase 2 features now fully integrated into main documentation
- Main `README.md` covers Phase 2 workflow coordination
- Main `QUICK_START.md` includes all Phase 2 commands
- `CLAUDE.md` documents Phase 2A implementation
- Kept for historical reference only

**Dependencies**:
- `verify_integration.sh` references these files (script should be archived too)
- `README_PHASE2.md` cross-references `QUICK_START_PHASE2.md`

**Action**:
```bash
mkdir -p docs/archive/phase2
mv README_PHASE2.md docs/archive/phase2/
mv QUICK_START_PHASE2.md docs/archive/phase2/
mv PHASE2_IMPLEMENTATION_SUMMARY.md docs/archive/phase2/
mv INTEGRATION_SUMMARY.md docs/archive/phase2/
mv verify_integration.sh docs/archive/phase2/
```

**Risk**: LOW - Only referenced by each other and by archived verification script

#### Phase 2A Documentation (2 files)

**Files**:
- `QUICK_START_PHASE_2A.md` (Phase 2A minimal workflow tracking)
- `PHASE_2A_IMPLEMENTATION_SUMMARY.md` (Implementation details)

**Reasoning**:
- Phase 2A is fully documented in `CLAUDE.md` (lines 52-206)
- Workflow tracking now standard feature
- Main `QUICK_START.md` covers workflow commands
- Historical value only

**Action**:
```bash
mv QUICK_START_PHASE_2A.md docs/archive/phase2/
mv PHASE_2A_IMPLEMENTATION_SUMMARY.md docs/archive/phase2/
```

**Risk**: ZERO - Fully superseded by CLAUDE.md and main docs

#### Delivery Documentation (2 files)

**Files**:
- `DELIVERABLES.md` (Project deliverables tracking)
- `COMPACTION_DELIVERY.md` (Compaction feature delivery notes)

**Reasoning**:
- Project milestone tracking (historical)
- Delivery documentation not needed for ongoing development
- Compaction feature not used in production

**Action**:
```bash
mkdir -p docs/archive/deliverables
mv DELIVERABLES.md docs/archive/deliverables/
mv COMPACTION_DELIVERY.md docs/archive/deliverables/
```

**Risk**: ZERO - Historical project management artifacts

### 2.2 Legacy Claude-Squad Commands

**Files** (9 commands in `/commands/`):
- `squad-assemble.md`
- `squad-deploy.md`
- `squad-dismiss.md`
- `squad-furlough.md`
- `squad-off.md`
- `squad-on.md`
- `squad-override.md`
- `squad-standdown.md`
- `squad-status.md`

**Reasoning**:
- Original claude-squad plugin management commands
- OaK system uses different workflow (telemetry-based, not plugin-based)
- Only `hooks/sessionStart.sh` references squad-on/squad-off (legacy hook)
- New system uses `oak-*` commands, not `squad-*` commands
- README.md doesn't reference any squad commands
- CLAUDE.md doesn't reference squad commands

**Dependencies**:
- `hooks/sessionStart.sh` checks for squad enablement (legacy mechanism)
- No other active code references these commands

**Action**:
```bash
mkdir -p docs/archive/claude-squad-legacy
mv commands/squad-*.md docs/archive/claude-squad-legacy/
# Note: commands/ directory will be empty after this
```

**Risk**: LOW - Original claude-squad commands, not used in OaK workflow

**Recommendation**: Update `hooks/sessionStart.sh` to remove squad references

### 2.3 Agent Creation Reports

**Files**:
- `agents/ux-designer-REPORT.md` (457 lines - creation report)

**Reasoning**:
- Creation report for `ux-designer.md` agent
- Historical artifact from agent-creator
- Not referenced in agent usage
- Separate from actual agent file

**Action**:
```bash
mkdir -p docs/archive/agent-reports
mv agents/ux-designer-REPORT.md docs/archive/agent-reports/
```

**Risk**: ZERO - Report file, not the agent itself

---

## Category 3: CONDITIONAL REMOVAL (Needs Confirmation)

### 3.1 Compaction Feature (Unused?)

**Files** (5 files in `/core/`):
- `core/compaction.py` (Context compression implementation)
- `core/test_compaction.py` (Unit tests)
- `core/validate_compaction.py` (Validation script)
- `core/COMPACTION_README.md` (Feature documentation)
- `core/COMPACTION_QUICK_START.md` (Usage guide)
- `core/COMPACTION_SUMMARY.md` (Summary)
- `core/INTEGRATION_GUIDE.md` (Integration instructions)
- `examples/compaction_workflow.py` (Example usage)

**Current Usage Analysis**:
- **Production code**: NO imports found outside core/
- **Scripts**: Only referenced by its own test files
- **Documentation**: README.md mentions "context compression" once but no usage examples
- **Import pattern**: Only self-referential (test_compaction.py, validate_compaction.py, examples/compaction_workflow.py)

**Questions to Answer**:
1. Is this a planned feature not yet integrated?
2. Was this experimental code that should be removed?
3. Is this feature actively used but not imported directly?

**Recommendation**: Ask user for decision

**If REMOVE**:
```bash
mkdir -p docs/archive/experimental/compaction
mv core/compaction.py docs/archive/experimental/compaction/
mv core/test_compaction.py docs/archive/experimental/compaction/
mv core/validate_compaction.py docs/archive/experimental/compaction/
mv core/COMPACTION_*.md docs/archive/experimental/compaction/
mv core/INTEGRATION_GUIDE.md docs/archive/experimental/compaction/
mv examples/compaction_workflow.py docs/archive/experimental/compaction/
```

**If KEEP**:
- Add usage examples to main README.md
- Document integration in QUICK_START.md
- Create clear entry point for feature usage

**Risk**: MEDIUM - Feature may be planned for future use

---

## Category 4: CONSOLIDATION OPPORTUNITIES

### 4.1 Root-Level Quick Start Consolidation

**Current State**:
- `QUICK_START.md` (Main quick start - CANONICAL)
- `QUICK_START_PHASE2.md` → Archive
- `QUICK_START_PHASE_2A.md` → Archive
- `USER_GUIDE.md` (664 lines - Comprehensive user guide)

**Analysis**:
- `QUICK_START.md` covers basic setup (hooks, automation, commands)
- `USER_GUIDE.md` covers daily/weekly/monthly usage patterns
- Phase-specific quick starts duplicate main content
- No clear distinction between "quick start" vs "user guide"

**Recommendation**: Keep both QUICK_START.md and USER_GUIDE.md
- `QUICK_START.md`: Installation and first-time setup (< 30 min)
- `USER_GUIDE.md`: Ongoing usage patterns and workflows

**Improvement**:
- Add cross-references between docs
- Clarify purposes in each file's intro
- Update README.md to clearly distinguish the two

**Action**:
```bash
# No deletion - add clarity to existing files
# Update QUICK_START.md header to reference USER_GUIDE.md
# Update USER_GUIDE.md header to reference QUICK_START.md
# Update README.md documentation section to clarify purposes
```

### 4.2 Root-Level README Consolidation

**Current State**:
- `README.md` (630 lines - Main project README - CANONICAL)
- `README_PHASE2.md` → Archive
- `CLAUDE.md` (858 lines - Agent delegation rules - KEEP)

**Analysis**:
- `README.md` is comprehensive and current
- `README_PHASE2.md` duplicates Phase 2 sections
- `CLAUDE.md` serves different purpose (agent rules, not user docs)

**Recommendation**: Keep only README.md at root (after archiving README_PHASE2.md)

---

## Category 5: KEEP (Essential Files)

### 5.1 Essential Documentation (Root Level)

**Files**:
- `README.md` - Main project documentation ✅
- `QUICK_START.md` - Installation and setup guide ✅
- `USER_GUIDE.md` - Usage patterns and workflows ✅
- `CLAUDE.md` - Agent delegation rules (required by Claude Code) ✅

**Reasoning**: Core documentation for different audiences and purposes

### 5.2 Architecture & Design Documentation

**Files in `/docs/`**:
- `docs/CONTEXT_ENGINEERING_ARCHITECTURE.md` (1,889 lines - Comprehensive architecture)
- `docs/ADAPTIVE_SYSTEM_DESIGN.md` (605 lines - System design)
- `docs/METADATA_ONLY_PROMPTS.md` (510 lines - Prompt optimization)
- `docs/MULTI_FILE_AGENTS.md` (541 lines - Agent packaging)
- `docs/PRODUCTION_VALIDATION_PLAN.md` (399 lines - Validation plan)
- `docs/SUCCESS_METRICS_REFERENCE.md` - Metrics definitions
- `docs/MIGRATION_GUIDE.md` - Migration documentation
- `docs/ENABLE_METADATA_PROMPTS.md` - Feature enablement
- `docs/oak-design/` - Complete OaK architecture

**Reasoning**: Technical reference documentation for architecture and advanced features

### 5.3 Agent Definitions

**All agent files** in `/agents/` (except ux-designer-REPORT.md)

**Reasoning**: Active agent definitions used by system

### 5.4 Core Infrastructure

**Files**:
- `core/agent_loader.py`
- `core/generate_agent_metadata.py`
- All telemetry, scripts, hooks, automation

**Reasoning**: Active system components

---

## Implementation Plan

### Phase 1: Safe Deletions (Immediate)

**Execute Immediately** (zero risk):

```bash
# 1. Delete wrong-repository file
rm customer-feature-analysis.md

# 2. Archive Phase 2 documentation
mkdir -p docs/archive/phase2
mv README_PHASE2.md QUICK_START_PHASE2.md docs/archive/phase2/
mv PHASE2_IMPLEMENTATION_SUMMARY.md INTEGRATION_SUMMARY.md docs/archive/phase2/
mv QUICK_START_PHASE_2A.md PHASE_2A_IMPLEMENTATION_SUMMARY.md docs/archive/phase2/
mv verify_integration.sh docs/archive/phase2/

# 3. Archive delivery documentation
mkdir -p docs/archive/deliverables
mv DELIVERABLES.md COMPACTION_DELIVERY.md docs/archive/deliverables/

# 4. Archive legacy squad commands
mkdir -p docs/archive/claude-squad-legacy
mv commands/squad-*.md docs/archive/claude-squad-legacy/

# 5. Archive agent reports
mkdir -p docs/archive/agent-reports
mv agents/ux-designer-REPORT.md docs/archive/agent-reports/
```

**Result**:
- Remove 1 wrong-repository file (1,001 lines)
- Archive 16 historical/phase-specific files
- Clean root directory: 13 files → 4 canonical files
- Preserve all historical information in organized archive

### Phase 2: User Decision Required

**Compaction Feature** (5 core files + 3 docs):

**Question**: Is the compaction feature (context compression) planned for active use?

**If NO (experimental/abandoned)**:
```bash
mkdir -p docs/archive/experimental/compaction
mv core/compaction.py core/test_compaction.py core/validate_compaction.py docs/archive/experimental/compaction/
mv core/COMPACTION_*.md core/INTEGRATION_GUIDE.md docs/archive/experimental/compaction/
mv examples/compaction_workflow.py docs/archive/experimental/compaction/
```

**If YES (planned feature)**:
- Document integration in README.md
- Add usage examples to QUICK_START.md
- Move documentation to docs/ (not core/)

### Phase 3: Documentation Improvements

**Update remaining root files**:

1. **QUICK_START.md**:
   - Add reference to USER_GUIDE.md for ongoing usage
   - Remove Phase 2-specific sections (now in archive)

2. **USER_GUIDE.md**:
   - Add reference to QUICK_START.md for installation
   - Consolidate workflow documentation

3. **README.md**:
   - Update documentation section to clarify file purposes
   - Remove references to archived phase-specific docs
   - Add note about archived documentation location

4. **CLAUDE.md**:
   - Review for phase-specific references
   - Ensure squad command references are intentional (legacy support?)

### Phase 4: Cleanup Hooks

**Review and update**:

```bash
# Check hooks/sessionStart.sh for squad references
# Consider removing legacy squad enablement checks
# Ensure hooks reference correct documentation paths
```

---

## Before/After Comparison

### Root Directory Files

**BEFORE** (13 markdown files):
```
CLAUDE.md ✅ KEEP
COMPACTION_DELIVERY.md → Archive
DELIVERABLES.md → Archive
INTEGRATION_SUMMARY.md → Archive
PHASE2_IMPLEMENTATION_SUMMARY.md → Archive
PHASE_2A_IMPLEMENTATION_SUMMARY.md → Archive
QUICK_START.md ✅ KEEP
QUICK_START_PHASE2.md → Archive
QUICK_START_PHASE_2A.md → Archive
README.md ✅ KEEP
README_PHASE2.md → Archive
USER_GUIDE.md ✅ KEEP
customer-feature-analysis.md ❌ DELETE
```

**AFTER** (4 markdown files):
```
CLAUDE.md - Agent delegation rules
QUICK_START.md - Installation & setup
README.md - Main project documentation
USER_GUIDE.md - Usage patterns & workflows
```

### Commands Directory

**BEFORE**: 9 squad command files
**AFTER**: Empty (or remove directory)

### Core Directory

**BEFORE**: 8 files (including 4 compaction docs)
**AFTER**: 2-3 files (if compaction archived)

### Overall Impact

**Files**:
- Deletions: 1 file (wrong repo)
- Archives: 16-24 files (depending on compaction decision)
- Keeps: 4 root docs + essential infrastructure
- Net reduction: ~30-40% less root-level clutter

**Maintainability**:
- Clear canonical documentation
- Historical information preserved and organized
- Reduced confusion for new users
- Easier to find current documentation

**Risk Level**:
- Phase 1 (Safe Deletions): ZERO risk
- Phase 2 (Compaction): MEDIUM risk (needs confirmation)
- Phase 3 (Doc updates): LOW risk
- Phase 4 (Hook cleanup): LOW risk

---

## Validation Checklist

Before executing cleanup:

- [ ] Confirm customer-feature-analysis.md is in wrong repository
- [ ] Verify no external scripts reference phase-specific docs
- [ ] Decide on compaction feature fate
- [ ] Backup repository (git commit before cleanup)
- [ ] Test system after Phase 1 cleanup
- [ ] Update any CI/CD references to moved files
- [ ] Update documentation cross-references

After cleanup:

- [ ] Verify all agent files still load
- [ ] Test telemetry system functionality
- [ ] Confirm automation still works
- [ ] Validate all oak-* commands work
- [ ] Check README.md renders correctly
- [ ] Test hooks/sessionStart.sh if modified

---

## Recommended Execution Order

1. **Backup**: Create git commit of current state
2. **Phase 1**: Execute safe deletions and archives
3. **Test**: Verify system functionality
4. **Phase 2**: Get user decision on compaction, execute if approved
5. **Test**: Verify system still functional
6. **Phase 3**: Update documentation cross-references
7. **Phase 4**: Clean up hooks if needed
8. **Final Test**: Complete system validation
9. **Commit**: Create cleanup commit with clear message

---

## Questions for User

1. **Compaction Feature**: Is `core/compaction.py` experimental code to remove, or planned feature to document?

2. **Squad Commands**: Should legacy squad commands be kept for backward compatibility, or fully archived?

3. **Hook Updates**: Should `hooks/sessionStart.sh` be updated to remove squad references?

4. **Additional Files**: Are there any other files you suspect might be bloat that weren't identified?

5. **Archive Location**: Is `docs/archive/` the right location, or prefer different organization?

---

## Success Metrics

**Cleanup Success Indicators**:
- Root directory: 13 files → 4 files (69% reduction)
- Clear separation: current docs vs historical archives
- No broken references in active documentation
- All tests pass after cleanup
- System functionality unchanged

**Maintainability Improvements**:
- New users see only current, relevant documentation
- Historical information preserved and organized
- Clear canonical source for each documentation purpose
- Reduced cognitive load for repository navigation

---

## Appendix: File Size Analysis

### Largest Files (Documentation)

```
1889 lines - docs/CONTEXT_ENGINEERING_ARCHITECTURE.md (KEEP - architecture)
1538 lines - agents/ux-designer.md (KEEP - active agent)
1316 lines - agents/product-strategist.md (KEEP - active agent)
1294 lines - docs/oak-design/6_MONTH_DEPLOYMENT_PLAN.md (KEEP - roadmap)
1001 lines - customer-feature-analysis.md (DELETE - wrong repo)
 858 lines - CLAUDE.md (KEEP - agent rules)
 664 lines - USER_GUIDE.md (KEEP - user guide)
 630 lines - README.md (KEEP - main docs)
 605 lines - docs/ADAPTIVE_SYSTEM_DESIGN.md (KEEP - design doc)
```

**Analysis**: Large files are appropriate for their purpose. Only customer-feature-analysis.md is bloat.

### Archive Totals

**Phase-specific documentation**: ~2,500 lines (8 files)
**Legacy squad commands**: ~2,500 lines (9 files)
**Delivery documentation**: ~800 lines (2 files)
**Compaction (if archived)**: ~1,500 lines (8 files)
**Total archived**: 6,000-7,500 lines

**Impact**: Significant reduction in surface area for new users while preserving all historical information.

---

## Final Recommendation

**Execute Phase 1 immediately** (zero risk, high value):
- Delete customer-feature-analysis.md
- Archive phase-specific and legacy documentation
- Update root documentation cross-references

**Get user decision on Phase 2** (compaction feature)

**Result**: Cleaner, more maintainable repository with all historical information preserved and organized.

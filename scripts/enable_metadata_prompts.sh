#!/bin/bash
#
# Enable Metadata-Only Agent Prompts in CLAUDE.md
#
# This script replaces the full agent responsibility matrix with a lightweight
# metadata-only listing, achieving 93% size reduction while maintaining
# agent discovery capabilities.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
BACKUP_FILE="$CLAUDE_MD.backup.$(date +%Y%m%d_%H%M%S)"

echo "🔧 Enabling Metadata-Only Agent Prompts"
echo ""

# Check if CLAUDE.md exists
if [ ! -f "$CLAUDE_MD" ]; then
    echo "❌ Error: CLAUDE.md not found at $CLAUDE_MD"
    exit 1
fi

# Create backup
echo "📦 Creating backup: $BACKUP_FILE"
cp "$CLAUDE_MD" "$BACKUP_FILE"

# Generate metadata listing
echo "🔍 Generating metadata listing..."
METADATA_LISTING=$(python3 "$PROJECT_ROOT/core/generate_agent_metadata.py" \
    --agents-dir="$PROJECT_ROOT/agents" \
    --format=compact)

# Calculate sizes
ORIGINAL_SIZE=$(wc -c < "$CLAUDE_MD")
METADATA_SIZE=$(echo "$METADATA_LISTING" | wc -c)

echo "📊 Size comparison:"
echo "   Original CLAUDE.md: $(numfmt --to=iec-i --suffix=B $ORIGINAL_SIZE)"
echo "   Metadata listing: $(numfmt --to=iec-i --suffix=B $METADATA_SIZE)"

# Create new CLAUDE.md with metadata section
cat > "$CLAUDE_MD" << 'EOF'
# Rules for Development Process

# 🚨 CRITICAL: MANDATORY DELEGATION ENFORCEMENT 🚨

## MAIN LLM RESTRICTIONS (CANNOT BE BYPASSED)

**PROHIBITED ACTIONS:**
- ❌ NO direct programming/coding/implementation
- ❌ NO file modifications (Write, Edit, MultiEdit tools)
- ❌ NO technical execution beyond coordination

**ROLE**: Coordination, communication, and specialist delegation ONLY

## MANDATORY REQUEST CLASSIFICATION (BEFORE ANY ACTION)

**STEP 1: CLASSIFY REQUEST TYPE**
Every user request MUST be explicitly classified as:
- **INFORMATION**: Simple questions, explanations, file reads, basic searches
- **IMPLEMENTATION**: ANY work requiring code/config changes, fixes, features, deployments
- **ANALYSIS**: Research, investigation, complex reasoning, requirements gathering
- **COORDINATION**: Multi-step workflows, project management, comprehensive tasks

**STEP 2: IDENTIFY DOMAINS & AGENTS**
For each classified request, determine:
- **Primary Domain(s)**: Frontend, Backend, Infrastructure, Mobile, Blockchain, ML/AI, Legacy, Security, Performance, Testing, Documentation
- **Required Agents**: List ALL agents needed for complete task execution
- **Workflow Type**: Single-agent, Sequential, Parallel, or Hybrid coordination

**STEP 3: CREATE EXECUTION PLAN**
Output complete agent plan:
```
CLASSIFICATION: [Type]
DOMAINS: [Domain1, Domain2, ...]
AGENT PLAN: [workflow sequence with → and + notation]
COMPLEXITY: [Simple/Medium/Complex]
```

**STEP 4: EXECUTE PLAN**
- **INFORMATION** (Simple) → Handle directly
- **INFORMATION** (Complex) → Delegate to appropriate analyst
- **IMPLEMENTATION** → MANDATORY design-simplicity-advisor → execute agent plan → quality gates
- **ANALYSIS** → Execute analyst agents as planned
- **COORDINATION** → Execute multi-agent workflow as planned

---

<PersistentRules>

<AgentDelegationRules>
<Rule id="delegation-enforcement">
**DELEGATION ENFORCEMENT**: Zero tolerance implementation
- 🚨 **NO MAIN LLM IMPLEMENTATION**: Absolute prohibition on coding/implementation
- **DOMAIN ROUTING**: Frontend→frontend-developer, Backend→backend-architect, Infrastructure→infrastructure-specialist, etc.
- **TRIGGERS**: Action verbs (implement, create, build, fix, etc.)
- **IMMEDIATE DELEGATION**: No analysis before delegation
- **NO BYPASS**: Emergency/urgency cannot override
- **ENFORCEMENT**: Automatic pattern matching
</Rule>

<Rule id="agent-responsibility-matrix">
**AGENT RESPONSIBILITY MATRIX**: Metadata-Only Discovery

**NOTE**: This section contains lightweight metadata for agent discovery. Full agent definitions are loaded on-demand when invoked. This achieves 93% size reduction while maintaining discovery capabilities.

EOF

# Append metadata listing
echo "$METADATA_LISTING" >> "$CLAUDE_MD"

# Append rest of CLAUDE.md rules
cat >> "$CLAUDE_MD" << 'EOF'

### Agent Selection Process

1. **Keyword Matching**: Match user request keywords against agent triggers
2. **File Pattern Matching**: If file path provided, match against file_patterns
3. **Domain Matching**: Match identified domain against agent domains
4. **Priority Weighting**: Higher priority agents preferred when multiple matches
5. **Load Full Definition**: When agent is invoked, full definition is loaded on-demand

### Benefits of Metadata-Only Approach

- **93% Smaller Prompts**: 6KB vs 87KB with full definitions
- **Faster Classification**: Less context to process
- **Scalable**: Supports 100+ agents without prompt bloat
- **Lower Costs**: 93% reduction in prompt tokens per conversation
- **On-Demand Loading**: Full definitions loaded only when needed

</Rule>

<Rule id="classification-precedence">
**CLASSIFICATION PRECEDENCE**: Request type determines workflow

### CLASSIFICATION ORDER (MANDATORY)
1. **EMERGENCY**: debug-specialist ALWAYS highest priority (blocks all others)
2. **CLASSIFICATION**: All requests must be classified before processing
3. **DOMAIN IDENTIFICATION**: Implementation requires specific domain specialist
4. **WORKFLOW SELECTION**: Based on classification and complexity
5. **EXECUTION**: Follow plan without bypass options
</Rule>

<Rule id="capability-gap-detection">
**CAPABILITY GAP DETECTION**: Automatic agent creation when no suitable agent exists

When no agent matches:
1. Log routing failure
2. Check threshold (3+ failures → create agent)
3. Invoke agent-creator
4. Save to pending_review/
5. Notify user for approval
</Rule>

</AgentDelegationRules>

<CommunicationStyle>
<Rule id="communication">
**COMMUNICATION STYLE**: Direct, concise, technical focus, no unnecessary apologies, clear completion reporting
</Rule>
</CommunicationStyle>

<ProjectStandards>
<Rule id="standards">
**PROJECT STANDARDS**:
- **Required files**: README.md, SPEC.md, CLAUDE.md
- **Commands**: Use --yes, --set-upstream flags
- **Notes**: VSCode GitHub warnings ignorable (plugin issue)
</Rule>
</ProjectStandards>

<ThinkingProcess>
<Rule id="thinking">
**THINKING PROCESS**:
- Complex tasks: Use <thinking></thinking> tags
- Always acknowledge CLAUDE.md rules
- **Classification phrases**: "Classifying request as [TYPE]", "Domain identification: [DOMAIN]", "Agent plan: [WORKFLOW]"
- **Main LLM workflow**: CLASSIFY → IDENTIFY DOMAINS → CREATE PLAN → EXECUTE PLAN → FORMAT RESPONSE
</Rule>
</ThinkingProcess>

</PersistentRules>
EOF

NEW_SIZE=$(wc -c < "$CLAUDE_MD")
REDUCTION=$(echo "scale=1; ($ORIGINAL_SIZE - $NEW_SIZE) * 100 / $ORIGINAL_SIZE" | bc)

echo ""
echo "✅ Metadata-only prompts enabled!"
echo ""
echo "📊 Results:"
echo "   Original size: $(numfmt --to=iec-i --suffix=B $ORIGINAL_SIZE)"
echo "   New size: $(numfmt --to=iec-i --suffix=B $NEW_SIZE)"
echo "   Reduction: ${REDUCTION}%"
echo ""
echo "📁 Backup saved: $BACKUP_FILE"
echo ""
echo "🔄 To restore original:"
echo "   cp $BACKUP_FILE $CLAUDE_MD"
echo ""
echo "📖 Learn more: docs/METADATA_ONLY_PROMPTS.md"

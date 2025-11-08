# Analyze Code Complexity

Run comprehensive complexity analysis to identify over-engineering and suggest simplifications.

## Usage
/analyze-complexity [path] [--report-format json|markdown]

## What This Does
1. Analyzes codebase or specific path for complexity issues
2. Identifies over-abstraction and premature optimization
3. Calculates cyclomatic complexity metrics
4. Flags YAGNI violations (You Aren't Gonna Need It)
5. Suggests concrete simplifications
6. Generates detailed complexity report

## Example
/analyze-complexity src/auth --report-format markdown

## Agent Coordination
1. **design-simplicity-advisor**: Primary analysis agent
   - Scans code for complexity patterns
   - Identifies unnecessary abstractions
   - Calculates complexity scores
   - Recommends simplifications
2. **Main LLM**: Formats and presents report

## Output
Complexity Report Format:
```markdown
## Code Complexity Analysis Report

### Overview
- Files analyzed: 12
- Total complexity score: 156 (target: <100)
- Over-engineered patterns found: 7
- Simplification opportunities: 5

### Critical Issues
1. **Excessive Abstraction** - src/auth/provider.ts
   - 4 layers of abstraction for simple OAuth flow
   - Recommendation: Flatten to 2 layers, remove factory pattern
   - Complexity reduction: 45 → 15

2. **Premature Optimization** - src/utils/cache.ts
   - Complex LRU cache for 10-item dataset
   - Recommendation: Use simple Map() object
   - Complexity reduction: 80 → 5

### Moderate Issues
3. **Over-Generic Interface** - src/api/handler.ts
   - Generic handler supports 20 methods, only 3 used
   - Recommendation: Create specific handlers
   - Complexity reduction: 35 → 12

### Simplification Opportunities
- Remove unused abstractions: 3 files
- Simplify control flow: 4 functions
- Eliminate premature optimization: 2 modules

### Action Items
1. Refactor src/auth/provider.ts (HIGH PRIORITY)
2. Replace LRU cache with Map (MEDIUM)
3. Split generic handler into specific implementations (LOW)

### Metrics
- Average cyclomatic complexity: 13 (target: <10)
- Maximum nesting depth: 6 (target: <4)
- YAGNI violations: 7
- Maintainability index: 62/100 (target: >65)
```

Returns: Detailed analysis with actionable recommendations

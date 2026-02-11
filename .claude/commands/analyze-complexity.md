# Analyze Complexity

Identify over-engineering and suggest simplifications using the design-simplicity-advisor agent.

## Usage
/analyze-complexity [path]

## What This Does
1. Scans code for unnecessary abstractions and complexity
2. Calculates cyclomatic complexity and nesting depth
3. Identifies YAGNI violations
4. Suggests concrete simplifications with impact estimates

## Example
/analyze-complexity src/auth

## Output
Complexity report with:
- Overall complexity score
- Over-engineered patterns found
- Specific simplification recommendations with before/after complexity scores

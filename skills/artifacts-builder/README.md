# Artifacts Builder Skill

**Source**: Anthropic's artifacts-builder skill (https://github.com/anthropics/skills/tree/main/artifacts-builder)
**Purpose**: Create elaborate React/TypeScript HTML artifacts for claude.ai

---

## Overview

This skill enables creation of self-contained HTML artifacts using modern frontend technologies:
- **Framework**: React 18 + TypeScript
- **Build**: Vite (dev) + Parcel (bundling)
- **Styling**: Tailwind CSS 3.4.1 + shadcn/ui
- **Output**: Single HTML file with all assets inlined

## When to Use

**Use artifacts-builder skill for:**
- Claude.ai artifact requests
- Simple, standard React artifacts
- Projects using React 18 + TypeScript + shadcn/ui stack
- Single HTML output required
- Standard UI patterns (forms, dashboards, widgets)

**Use frontend-developer agent instead for:**
- Complex multi-page applications
- Custom architecture requirements
- Non-standard tech stacks
- Backend integration needed
- oak-specific workflow requirements

## Usage

### From Python
```python
from skills.artifacts_builder import invoke_artifact_skill

result = invoke_artifact_skill(
    artifact_name="user-dashboard",
    requirements="Create a todo list with checkboxes and local storage",
    mode="standard"  # or "custom"
)
```

### From Command Line
```bash
# Initialize new artifact project
cd skills/artifacts-builder
bash scripts/init-artifact.sh my-artifact

# Develop (in project directory)
cd my-artifact
pnpm dev

# Bundle to single HTML
bash ../../scripts/bundle-artifact.sh
# Output: bundle.html
```

## Workflow

1. **Initialize**: Create React + TypeScript + shadcn/ui project
2. **Develop**: Implement features using shadcn/ui components
3. **Bundle**: Package everything into single HTML file
4. **Present**: Share artifact with user
5. **Test** (optional): Validate functionality if needed

## Technical Details

### Stack
- React 18 (functional components + hooks)
- TypeScript (strict mode)
- Vite 5.4.11+ (Node 18+) or latest (Node 20+)
- Parcel (bundling)
- Tailwind CSS 3.4.1
- shadcn/ui (40+ pre-installed components)
- Path aliases (@/ for src/)

### Pre-installed Components
40+ shadcn/ui components available:
- Layout: Card, Separator, ScrollArea, Sheet
- Forms: Button, Input, Label, Checkbox, RadioGroup, Select, Textarea, Switch, Slider
- Data: Table, Badge, Avatar, Progress
- Overlays: Dialog, Popover, Tooltip, Sheet
- Navigation: Tabs, Menubar, NavigationMenu
- Feedback: Alert, Toast, Sonner

### Scripts

**init-artifact.sh** (323 lines):
- Node version detection (18+ required)
- pnpm installation if missing
- Vite project creation
- Tailwind CSS configuration
- shadcn/ui components extraction
- TypeScript path alias setup

**bundle-artifact.sh** (54 lines):
- Parcel bundler installation
- Build with no source maps
- Asset inlining (html-inline)
- Single HTML output

## Integration with oak Workflows

After skill execution:
1. **quality-gate** validates artifact (bundle size, design guidelines)
2. **git-workflow-manager** commits changes
3. User receives artifact + source code

## Design Guidelines

**Avoid "AI slop" patterns:**
- ❌ Excessive centered layouts
- ❌ Purple gradients everywhere
- ❌ Uniform rounded corners
- ❌ Inter font as default

**Use instead:**
- ✅ Varied, intentional layouts
- ✅ Purpose-driven color schemes
- ✅ Contextual styling choices
- ✅ Font selection based on purpose

## Requirements

- Node.js 18+ (20+ recommended)
- pnpm (auto-installed if missing)
- ~200MB disk space for dependencies

## License

See LICENSE.txt in artifacts-builder directory (Apache 2.0)

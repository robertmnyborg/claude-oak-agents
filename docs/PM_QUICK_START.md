# PM Quick Start Guide

**Get started with AI-powered product development in 10 minutes**

This guide provides 6 practical examples that demonstrate real PM workflows with claude-oak-agents. Each example includes the exact prompt to use, what happens behind the scenes, and what you'll get back.

## Prerequisites

- Claude Code installed and configured
- claude-oak-agents repository cloned
- Agents linked to `~/.claude/agents/`

If you haven't set up yet, see the [installation guide](../README.md#quick-start-5-minutes).

---

## Example 1: Co-Author a Feature Specification

**Use Case**: You need to document a new feature with clear requirements, technical design, and implementation plan.

### The Prompt

```
Help me create a spec for user authentication with OAuth2
```

### What Happens

The **spec-manager** agent guides you through collaborative specification writing:

1. **Goals & Requirements** - Define what we're building and why
   - Spec-manager asks clarifying questions
   - You approve each section before moving forward

2. **Technical Design** - How will it work?
   - Architecture decisions
   - Technology choices
   - Integration points

3. **Implementation Plan** - What needs to be built?
   - Task breakdown
   - Agent assignments
   - Time estimates

4. **Test Strategy** - How do we validate?
   - Test scenarios
   - Acceptance criteria
   - Success metrics

### What You Get

**Two files created**:
- `specs/active/2025-10-24-oauth2-auth.md` - Human-readable Markdown for collaboration
- `specs/active/2025-10-24-oauth2-auth.yaml` - Machine-readable YAML for execution

**Benefits**:
- Work in "spec terms" not "code terms"
- Approval checkpoints at each section
- Change tracking throughout implementation
- Complete context for engineering handoff

### Follow-Up Actions

```
# Review the spec
"Show me the OAuth2 spec we created"

# Make changes
"Update spec section 2.3 - use JWT tokens instead of session cookies"

# Execute the spec
"Implement the OAuth2 spec"
```

---

## Example 2: Design a Database Schema

**Use Case**: You're designing data models for a new feature and need a normalized schema with proper relationships and indexes.

### The Prompt

```
Design a PostgreSQL schema for a multi-tenant SaaS application with organizations, users, and projects
```

### What Happens

The **backend-architect** agent:

1. Analyzes requirements and data relationships
2. Creates normalized schema with proper foreign keys
3. Designs indexes for query performance
4. Generates DDL statements
5. Plans migration strategy

### What You Get

**Database Design**:

```sql
-- Organizations table (tenant isolation)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_organizations_slug ON organizations(slug);

-- Users table (belongs to organization)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(organization_id, email)
);

CREATE INDEX idx_users_org_id ON users(organization_id);
CREATE INDEX idx_users_email ON users(email);

-- Projects table (belongs to organization)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_projects_org_id ON projects(organization_id);
CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
```

**Migration Plan**:
- Step 1: Create organizations table
- Step 2: Create users table with foreign key
- Step 3: Create projects table with foreign keys
- Step 4: Add indexes
- Step 5: Seed initial data

**Performance Considerations**:
- Composite indexes for common query patterns
- CASCADE deletes for tenant isolation
- UUIDs for distributed systems
- Timestamp tracking for audit

### Follow-Up Actions

```
# Generate migrations
"Create Alembic migrations for this schema"

# Add more tables
"Add a tasks table that belongs to projects"

# Optimize queries
"What indexes do I need for queries filtering projects by status and organization?"
```

---

## Example 3: Create a Redux Store

**Use Case**: You need a state management solution for a React application feature.

### The Prompt

```
Design a Redux store for shopping cart state with add/remove/update quantity actions
```

### What Happens

The **frontend-developer** agent:

1. Creates state slice with TypeScript types
2. Defines actions and action creators
3. Implements reducers with immutable updates
4. Adds selectors for accessing state
5. Provides usage examples

### What You Get

**Redux Slice** (`src/store/cartSlice.ts`):

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Types
interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
  imageUrl: string;
}

interface CartState {
  items: CartItem[];
  totalItems: number;
  totalPrice: number;
}

// Initial state
const initialState: CartState = {
  items: [],
  totalItems: 0,
  totalPrice: 0,
};

// Slice
const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<CartItem>) => {
      const existingItem = state.items.find(
        item => item.productId === action.payload.productId
      );

      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
      } else {
        state.items.push(action.payload);
      }

      // Recalculate totals
      state.totalItems = state.items.reduce((sum, item) => sum + item.quantity, 0);
      state.totalPrice = state.items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
      );
    },

    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(item => item.productId !== action.payload);

      // Recalculate totals
      state.totalItems = state.items.reduce((sum, item) => sum + item.quantity, 0);
      state.totalPrice = state.items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
      );
    },

    updateQuantity: (
      state,
      action: PayloadAction<{ productId: string; quantity: number }>
    ) => {
      const item = state.items.find(
        item => item.productId === action.payload.productId
      );

      if (item) {
        item.quantity = action.payload.quantity;

        // Recalculate totals
        state.totalItems = state.items.reduce((sum, item) => sum + item.quantity, 0);
        state.totalPrice = state.items.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        );
      }
    },

    clearCart: (state) => {
      state.items = [];
      state.totalItems = 0;
      state.totalPrice = 0;
    },
  },
});

// Actions
export const { addItem, removeItem, updateQuantity, clearCart } = cartSlice.actions;

// Selectors
export const selectCartItems = (state: RootState) => state.cart.items;
export const selectTotalItems = (state: RootState) => state.cart.totalItems;
export const selectTotalPrice = (state: RootState) => state.cart.totalPrice;
export const selectItemByProductId = (productId: string) => (state: RootState) =>
  state.cart.items.find(item => item.productId === productId);

// Reducer
export default cartSlice.reducer;
```

**Usage Examples**:

```typescript
// In a component
import { useDispatch, useSelector } from 'react-redux';
import { addItem, selectCartItems, selectTotalPrice } from './store/cartSlice';

function ProductCard({ product }) {
  const dispatch = useDispatch();

  const handleAddToCart = () => {
    dispatch(addItem({
      productId: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
      imageUrl: product.imageUrl,
    }));
  };

  return <button onClick={handleAddToCart}>Add to Cart</button>;
}

function CartSummary() {
  const items = useSelector(selectCartItems);
  const totalPrice = useSelector(selectTotalPrice);

  return (
    <div>
      <h3>Cart ({items.length} items)</h3>
      <p>Total: ${totalPrice.toFixed(2)}</p>
    </div>
  );
}
```

### Follow-Up Actions

```
# Add persistence
"Add localStorage persistence to the cart store"

# Add async actions
"Add a checkout action that calls the /api/checkout endpoint"

# Add optimistic updates
"Implement optimistic UI updates for add/remove actions"
```

---

## Example 4: Map a User Workflow

**Use Case**: You need to understand user journey through a feature and identify friction points.

### The Prompt

```
Map the user workflow for password reset from forgot password through successful login
```

### What Happens

The **ux-designer** agent:

1. Breaks down the workflow into steps
2. Identifies decision points and error states
3. Maps user actions to system responses
4. Highlights potential friction points
5. Suggests improvements based on UX principles

### What You Get

**User Workflow Map**:

```
PASSWORD RESET WORKFLOW
=======================

Step 1: Initiate Reset
┌─────────────────────────────────┐
│ User on Login Page              │
│ ↓ Clicks "Forgot Password?"     │
└─────────────────────────────────┘
          ↓
┌─────────────────────────────────┐
│ Reset Request Page              │
│ • Input: Email address          │
│ • Button: "Send Reset Link"     │
│                                 │
│ Validation:                     │
│ - Email format                  │
│ - Rate limiting (max 3/hour)    │
└─────────────────────────────────┘
          ↓
┌─────────────────────────────────┐
│ Confirmation Page               │
│ "Check your email for reset     │
│  link (expires in 1 hour)"      │
│                                 │
│ UX NOTE: Show this even if      │
│ email not found (security)      │
└─────────────────────────────────┘

Step 2: Email & Click Link
┌─────────────────────────────────┐
│ Email Received                  │
│ Subject: "Reset Your Password"  │
│ ↓ User clicks link              │
└─────────────────────────────────┘
          ↓
┌─────────────────────────────────┐
│ Token Validation                │
│                                 │
│ Error States:                   │
│ ❌ Link expired (>1 hour)       │
│ ❌ Link already used            │
│ ❌ Invalid token                │
│ → Redirect to request new       │
└─────────────────────────────────┘
          ↓ ✅ Valid

Step 3: Reset Password
┌─────────────────────────────────┐
│ New Password Page               │
│ • Input: New password           │
│ • Input: Confirm password       │
│ • Button: "Reset Password"      │
│                                 │
│ Requirements Visible:           │
│ - 8+ characters                 │
│ - 1 uppercase                   │
│ - 1 number                      │
│ - 1 special character           │
│                                 │
│ Real-time validation feedback   │
└─────────────────────────────────┘
          ↓
┌─────────────────────────────────┐
│ Success & Auto-Login            │
│ "Password updated!"             │
│ ↓ Auto-redirect to dashboard    │
│   (session created)             │
└─────────────────────────────────┘

FRICTION POINTS IDENTIFIED
===========================

🔴 High Friction:
1. Token expiration (1 hour) - Users often don't check email immediately
   → Recommendation: Extend to 24 hours

2. No progress indicator on email send
   → Recommendation: Add "Sending..." state

🟡 Medium Friction:
3. Password requirements not visible before clicking link
   → Recommendation: Show in reset request confirmation

4. No option to copy/paste into confirm password field
   → Recommendation: Allow paste, add "Show Password" toggle

🟢 Low Friction:
5. Success state could be more celebratory
   → Recommendation: Add success animation + clear next action

ERROR RECOVERY PATHS
====================

Expired Token:
  → Show: "Reset link expired. Request a new one?"
  → Pre-fill email from token
  → One-click re-request

Invalid Token:
  → Show: "This link is invalid. Need a reset link?"
  → Link to request page

Rate Limited:
  → Show: "Too many requests. Try again in X minutes."
  → Show countdown timer
  → Suggest contacting support if urgent

UX IMPROVEMENTS
===============

Priority 1 (Easy Wins):
- Add loading states to all buttons
- Show password requirements upfront
- Extend token expiration to 24 hours
- Add "Show Password" toggle

Priority 2 (Nice to Have):
- Email preview of password change
- Option to reset from multiple devices
- Remember browser for 30 days
- Biometric authentication option
```

### Follow-Up Actions

```
# Create wireframes
"Create wireframe mockups for the password reset flow"

# Analyze specific friction
"What's the best way to handle expired tokens?"

# Benchmark competitors
"How do major SaaS apps handle password reset? Show best practices."
```

---

## Example 5: Fork Repo and Create Pull Request

**Use Case**: You've prototyped a feature and need to create a professional handoff to engineering.

### The Prompt

```
Fork the production repo, create a feature branch for OAuth2, commit the spec and schema, and open a PR
```

### What Happens

The **git-workflow-manager** agent:

1. Forks the repository (if needed)
2. Creates feature branch with clear naming
3. Stages and commits files with descriptive message
4. Pushes to remote with proper upstream tracking
5. Creates pull request with complete context

### What You Get

**Git Operations**:

```bash
# Branch created
feature/oauth2-authentication

# Files committed
git add specs/active/2025-10-24-oauth2-auth.md
git add specs/active/2025-10-24-oauth2-auth.yaml
git add migrations/001_create_auth_tables.sql
git add docs/oauth2_implementation_notes.md

# Commit message
feat: Add OAuth2 authentication specification and database schema

Comprehensive spec for OAuth2 authentication including:
- Requirements and user stories
- Technical architecture with JWT tokens
- Database schema for users and sessions
- Migration plan and rollback strategy
- Security considerations and compliance notes

Ready for engineering review and implementation estimation.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>

# PR created with description
```

**Pull Request** (automatically opened):

```markdown
## OAuth2 Authentication Specification

### Summary
Complete specification for implementing OAuth2 authentication with JWT tokens.
Includes database schema, migration plan, and security considerations.

### Files Included
- `specs/active/2025-10-24-oauth2-auth.md` - Human-readable spec
- `specs/active/2025-10-24-oauth2-auth.yaml` - Machine-readable execution plan
- `migrations/001_create_auth_tables.sql` - Database migrations
- `docs/oauth2_implementation_notes.md` - Technical notes

### Acceptance Criteria
- [ ] OAuth2 authorization code flow implemented
- [ ] JWT token generation and validation
- [ ] Refresh token rotation
- [ ] Database schema deployed to staging
- [ ] Unit tests for token validation
- [ ] Integration tests for full auth flow
- [ ] Security audit completed
- [ ] Documentation updated

### Implementation Notes
- Estimated complexity: Medium (3-5 days)
- Dependencies: None (isolated feature)
- Backwards compatible: Yes (new tables, no schema changes)
- Feature flag recommended: `oauth2_enabled`

### Test Plan
- Unit tests for token generation/validation
- Integration tests for OAuth2 flow
- Security tests for token expiration
- Load tests for auth endpoints

### Rollout Strategy
1. Deploy to dev environment
2. Internal testing (QA team)
3. Deploy to staging with feature flag off
4. Enable for beta users (10%)
5. Monitor error rates and latency
6. Gradual rollout to 100%

🤖 Generated with Claude Code
```

### Follow-Up Actions

```
# Check PR status
"What's the status of the OAuth2 PR?"

# Address review feedback
"Update the PR based on engineering feedback: use Redis for token storage instead of database"

# Create related PRs
"Create a separate PR for the frontend OAuth2 login flow"
```

---

## Example 6: Translate Business Problem to Product Strategy

**Use Case**: Stakeholders have a business problem and you need to frame it as a product opportunity with clear success metrics.

### The Prompt

```
Customer churn rate is 15% monthly. Help me frame this as a product problem and define solutions with success metrics.
```

### What Happens

The **product-strategist** agent uses the Eigenquestion methodology:

1. Reframes business problem as "eigenquestion"
2. Identifies root causes and evidence
3. Generates solution hypotheses
4. Defines validation experiments
5. Establishes success metrics

### What You Get

**Strategic Framework**:

```markdown
# EIGENQUESTION ANALYSIS: Customer Churn

## The Eigenquestion

"What causes customers to stop getting value from our product within their first 3 months?"

Why this framing matters:
- Focus on VALUE DELIVERY not just retention
- Timebound (first 3 months = critical activation period)
- Root cause oriented (WHY they churn, not just THAT they churn)
- Actionable (we can improve value delivery)

## Evidence & Root Causes

### Quantitative Evidence
- 15% monthly churn rate (industry avg: 5-7%)
- 68% of churned customers never completed onboarding
- 82% of churned customers used <3 core features
- Avg time to first value: 18 days (target: <7 days)

### Qualitative Evidence (from exit interviews)
- "Too complicated to set up" (42%)
- "Didn't understand how to use it" (31%)
- "Didn't see value fast enough" (19%)
- "Switched to competitor" (8%)

### Root Causes Identified
1. **Activation failure** - Users don't complete onboarding
2. **Value gap** - Time to first value too long
3. **Feature discovery** - Users don't find relevant features
4. **Complexity** - Product perceived as too difficult

## Solution Hypotheses

### Hypothesis 1: Guided Onboarding
**Assumption**: Customers churn because they don't complete setup

**Experiment**: Implement progressive onboarding wizard
- Step 1: Import data (5 min)
- Step 2: Configure first workflow (10 min)
- Step 3: See first result (immediate)

**Success Metric**:
- Onboarding completion rate: 68% → 85%
- Time to first value: 18 days → 7 days
- 30-day retention: 85% → 92%

**Validation**: A/B test over 4 weeks with 1000 new users

### Hypothesis 2: Value Demonstration
**Assumption**: Customers churn because they don't see ROI fast enough

**Experiment**: Add "Quick Wins" dashboard
- Show time saved in first week
- Highlight automated tasks
- Display cost savings calculation

**Success Metric**:
- % users viewing value dashboard: Track baseline → 60%+
- Feature adoption (3+ features): 18% → 40%
- Upgrade rate (free → paid): 12% → 18%

**Validation**: Feature flag rollout, measure over 8 weeks

### Hypothesis 3: Personalized Feature Discovery
**Assumption**: Customers churn because product feels generic

**Experiment**: Role-based feature recommendations
- Segment users by role/industry
- Show relevant features first
- Hide irrelevant complexity

**Success Metric**:
- Feature discovery rate: Track baseline → 50% improvement
- Features used per user: 2.1 → 4.5
- NPS score: 32 → 45

**Validation**: Cohort analysis over 12 weeks

## Prioritization Matrix

| Hypothesis | Impact | Effort | Confidence | Priority |
|-----------|--------|--------|-----------|----------|
| Guided Onboarding | HIGH | Medium | HIGH | P0 (Ship first) |
| Value Demonstration | HIGH | Low | Medium | P0 (Ship first) |
| Personalized Discovery | Medium | HIGH | Low | P1 (Ship after validation) |

## Success Metrics (North Star)

### Primary Metric
**30-Day Retention Rate**
- Current: 85%
- Target: 92% (7% improvement = -50% relative churn)
- Timeline: 3 months

### Secondary Metrics
- Onboarding completion: 68% → 85%
- Time to first value: 18 days → 7 days
- Features used per user: 2.1 → 4.5
- Customer satisfaction (NPS): 32 → 45

### Leading Indicators (Weekly Tracking)
- Day 1 activation rate
- Week 1 active users
- Onboarding step completion
- Value dashboard views

## Roadmap

### Month 1: Quick Wins
- Week 1-2: Ship guided onboarding (P0)
- Week 3-4: Ship value dashboard (P0)

### Month 2: Validation
- Measure impact on retention
- Collect user feedback
- Iterate based on data

### Month 3: Scale or Pivot
- If working (retention >90%): Scale to all users
- If not working (retention <88%): Investigate Hypothesis 3

## Risk Mitigation

### Risk 1: Onboarding Complexity
- Mitigation: User test with 20 customers before launch
- Fallback: Skip onboarding option for power users

### Risk 2: Value Metrics Misleading
- Mitigation: Validate calculations with finance team
- Fallback: Qualitative testimonials if quantitative weak

### Risk 3: Feature Bloat
- Mitigation: Hide advanced features behind "Show More"
- Fallback: Role-based UI if progressive disclosure insufficient
```

### Follow-Up Actions

```
# Create detailed product brief
"Create a product brief for the guided onboarding feature with user stories"

# Design validation experiment
"Design an A/B test plan for the value dashboard experiment"

# Estimate engineering effort
"What's the technical complexity of implementing role-based feature discovery?"
```

---

## Next Steps

### Practice These Workflows

Start with Example 1 (co-author a spec) and work through each example. The agents get better as they learn from your feedback and patterns.

### Combine Examples

Real PM work often combines multiple workflows:

```
"Create a spec for the guided onboarding feature,
design the database schema for tracking onboarding progress,
design the Redux store for onboarding state,
and create a PR with everything"
```

The agents will coordinate to deliver a complete package.

### Explore More

- **[PM Workflows Library](PM_WORKFLOWS.md)** - More patterns and examples
- **[PM Capabilities Matrix](PM_CAPABILITIES.md)** - What works vs what's manual
- **[USER_GUIDE.md](../USER_GUIDE.md)** - Complete system documentation

### Get Help

- **Questions**: [GitHub Discussions](https://github.com/robertmnyborg/claude-oak-agents/discussions)
- **Issues**: [GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)
- **Community**: Join the PM community discussion

---

**Ready to try your first workflow?** Start with Example 1 and create your first spec!

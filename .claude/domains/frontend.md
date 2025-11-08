---
domain: frontend
priority: 1
primary_agent: frontend-developer
secondary_agents: [qa-specialist, git-workflow-manager]
related_agents: [spec-manager, systems-architect, dependency-scanner]
---

# Domain: Frontend Development

## Tech Stack

### Core Technologies
**Frameworks**: React 18+, Vue 3, Next.js - [See State of JS 2024 comparison](https://2024.stateofjs.com/en-US/libraries/front-end-frameworks/)
**Languages**: TypeScript (strict mode), JavaScript ES2022+
**Build Tools**: Vite, Webpack 5 - [Complete build tool comparison](https://webpack.js.org/concepts/why-webpack/)
**Package Manager**: Yarn 3.5.1 (Berry), npm

### State Management (Top 5)
React: **Redux Toolkit**, Zustand, TanStack Query, Context API, Pinia
Vue: **Pinia**, Composition API, Vuex 4
[See more options](https://thenewstack.io/redux-alternatives-how-to-manage-state-in-javascript-apps/)

### Styling Solutions
**CSS Frameworks**: Tailwind CSS, Bootstrap 5
**CSS-in-JS**: Styled Components, Emotion, CSS Modules
[See styling comparison](https://www.sitepoint.com/react-css-styling-options/)

### UI Libraries (Top 5)
React: **Material-UI (MUI)**, Chakra UI, Ant Design, Shadcn/ui
Vue: **Vuetify**, Quasar, Element Plus

### Testing & Quality (Top 3)
**Unit Testing**: Jest, Vitest, React Testing Library
**E2E Testing**: Cypress, Playwright
**Quality**: ESLint, Prettier, TypeScript strict mode

## Patterns & Conventions

### Component Architecture
1. **Composition Over Inheritance**: Favor component composition
2. **Atomic Design**: Atoms → Molecules → Organisms → Templates → Pages
3. **Functional Components**: Use hooks over class components (React)
4. **Single Responsibility**: One component, one purpose
5. **Props Drilling Avoidance**: Use context or state management for deep props

### Code Organization
```
src/
├── components/          # Reusable UI components
│   ├── atoms/          # Basic building blocks
│   ├── molecules/      # Composite components
│   └── organisms/      # Complex components
├── pages/              # Route components
├── hooks/              # Custom React hooks
├── utils/              # Helper functions
├── services/           # API services
├── store/              # State management
├── types/              # TypeScript definitions
├── styles/             # Global styles
└── assets/             # Static assets
```

### Naming Conventions
- **Components**: PascalCase (`UserProfile.tsx`)
- **Hooks**: camelCase with 'use' prefix (`useAuth.ts`)
- **Utils**: camelCase (`formatDate.ts`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`)
- **CSS Modules**: camelCase for classes

### State Management Best Practices
1. **Local State First**: Use component state when possible
2. **Server State**: TanStack Query for data fetching
3. **Global State**: Redux/Zustand/Pinia for cross-component state
4. **Form State**: React Hook Form, Formik, VeeValidate
5. **URL State**: React Router, Vue Router for navigation state

### Performance Patterns
1. **Code Splitting**: Dynamic imports for routes and large components
2. **Lazy Loading**: `React.lazy()`, Vue `defineAsyncComponent()`
3. **Memoization**: `useMemo`, `useCallback`, `memo` (React)
4. **Virtual Scrolling**: For large lists (react-window, vue-virtual-scroller)
5. **Bundle Optimization**: Tree shaking, chunk splitting

### Accessibility Standards
1. **WCAG 2.1 AA Compliance**: Minimum accessibility standard
2. **Semantic HTML**: Use appropriate HTML5 elements
3. **ARIA Attributes**: When semantic HTML is insufficient
4. **Keyboard Navigation**: Full keyboard support
5. **Screen Reader Testing**: Test with NVDA, JAWS, VoiceOver

## File Structure & Organization

### Monorepo Structure (Turborepo)
```
apps/
  web/                  # Main web application
  docs/                 # Storybook documentation
  embed/                # Embedded widgets
libs/
  ui/                   # Shared UI components
  utils/                # Shared utilities
  config/               # Shared configs (ESLint, TS)
tools/
  build-config/         # Build tool configs
```

### Feature-Based Structure
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── types/
```

## Agent Workflows

### Simple Component Implementation
**Trigger**: "Create a button component", "Add form validation"
```
frontend-developer → qa-specialist → git-workflow-manager
```

### New Feature Development
**Trigger**: "Build user dashboard", "Implement shopping cart"
```
spec-manager → frontend-developer → qa-specialist → git-workflow-manager
```

### Complex Feature with State
**Trigger**: "Multi-step form with validation", "Real-time data dashboard"
```
spec-manager → systems-architect → frontend-developer → qa-specialist → dependency-scanner → git-workflow-manager
```

### Performance Optimization
**Trigger**: "Optimize bundle size", "Improve initial load time"
```
frontend-developer (analysis) → frontend-developer (implementation) → qa-specialist
```

### Accessibility Enhancement
**Trigger**: "Make form accessible", "Add ARIA labels"
```
frontend-developer → qa-specialist (accessibility testing)
```

## Triggers

### Keywords
- **Component-related**: component, widget, UI, interface, layout, template
- **Framework-specific**: React, Vue, Angular, Next.js, Nuxt, hooks, composition
- **State-related**: state, store, Redux, Zustand, Pinia, context
- **Styling**: CSS, Tailwind, styled-components, theme, responsive
- **Interaction**: form, validation, animation, transition, modal, dropdown
- **Data**: fetch, query, API call, data loading, cache
- **Testing**: unit test, E2E, Cypress, Jest, test coverage

### File Patterns
- `*.tsx`, `*.jsx` - React components
- `*.vue` - Vue components
- `*.component.ts` - Angular components
- `src/components/**/*`
- `src/pages/**/*`
- `src/hooks/**/*`
- `src/store/**/*`
- `*.module.css`, `*.scss`
- `*.test.tsx`, `*.spec.ts`

### Tech Stack Mentions
- React, Vue, Angular, Svelte
- TypeScript, JavaScript
- Vite, Webpack, Rollup
- Tailwind, Material-UI, Chakra
- Redux, TanStack Query

## Quality Standards

### Code Quality
- **TypeScript Strict Mode**: Enable all strict flags
- **ESLint Rules**: Zero warnings/errors
- **Prettier Formatting**: Consistent code style
- **No Console Logs**: Remove debug statements
- **Type Coverage**: 100% type safety

### Testing Requirements
- **Unit Test Coverage**: 80%+ for components
- **Integration Tests**: Critical user flows
- **E2E Tests**: Main user journeys
- **Accessibility Tests**: Automated a11y checks (jest-axe)
- **Visual Regression**: Storybook visual tests

### Performance Metrics
- **First Contentful Paint (FCP)**: < 1.8s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Time to Interactive (TTI)**: < 3.8s
- **Cumulative Layout Shift (CLS)**: < 0.1
- **Bundle Size**: < 250KB initial (gzipped)

### Browser Support
- **Modern Browsers**: Chrome, Firefox, Safari, Edge (last 2 versions)
- **Mobile**: iOS Safari 14+, Chrome Mobile
- **Progressive Enhancement**: Core functionality without JS
- **Polyfills**: Only when necessary (use @babel/preset-env)

## Common Tasks & Solutions

### Creating a New Component
1. Define component interface (TypeScript types)
2. Implement component with proper hooks
3. Add CSS/styling (Tailwind/CSS Modules)
4. Write unit tests (React Testing Library)
5. Document in Storybook (if applicable)
6. Export from index file

### Setting Up Data Fetching
1. Use TanStack Query for server state
2. Define API service functions
3. Create custom hooks (`useFetchUser`)
4. Handle loading/error states
5. Implement optimistic updates if needed
6. Add error boundaries

### Form Implementation
1. Use React Hook Form or Formik
2. Define validation schema (Zod, Yup)
3. Create reusable form components
4. Handle submission and errors
5. Add accessibility labels
6. Implement loading states

### State Management Setup
1. Choose appropriate solution (local vs global)
2. Define state shape (TypeScript interfaces)
3. Create store/context
4. Implement actions/mutations
5. Add selectors/computed properties
6. Test state logic

## Integration Points

### Backend Integration
- **API Communication**: Fetch API, Axios, TanStack Query
- **Authentication**: JWT tokens, OAuth flows
- **WebSockets**: Socket.io, native WebSockets
- **GraphQL**: Apollo Client, urql

### Infrastructure Integration
- **Build & Deploy**: Vite build, CDK deployment to S3+CloudFront
- **Environment Variables**: `.env` files, build-time injection
- **CDN**: Static asset optimization
- **Error Tracking**: Sentry, LogRocket

### Security Considerations
- **XSS Prevention**: Sanitize user input, use dangerouslySetInnerHTML sparingly
- **CSRF Protection**: Anti-CSRF tokens
- **Content Security Policy**: Proper CSP headers
- **Dependency Scanning**: Regular npm audit, Snyk

## Domain-Specific Commands

### Development
```bash
# Start dev server
yarn dev / npm run dev

# Type checking
yarn type:check / tsc --noEmit

# Linting
yarn lint / eslint src/
yarn lint:fix

# Formatting
yarn format / prettier --write src/
```

### Testing
```bash
# Unit tests
yarn test / npm test
yarn test:watch
yarn test:coverage

# E2E tests
yarn test:e2e
yarn cypress:open
yarn playwright test
```

### Build & Deploy
```bash
# Build for production
yarn build

# Preview production build
yarn preview

# Analyze bundle
yarn analyze

# Deploy (CDK)
yarn synth
yarn deploy
```

## Decision Framework

### When to Use This Domain
- ✅ Building user interfaces
- ✅ Implementing client-side logic
- ✅ Creating interactive components
- ✅ Optimizing frontend performance
- ✅ Implementing responsive design
- ✅ Adding accessibility features

### When to Coordinate with Other Domains
- **Backend**: API contract design, data fetching patterns
- **Infrastructure**: Build configuration, deployment pipelines
- **Security**: Authentication flows, input validation
- **Data**: Query optimization, caching strategies

## Example Scenarios

### Scenario 1: Simple UI Component
**Request**: "Create a reusable button component with variants"

**Domain Detection**: Frontend (keywords: component, button)

**Workflow**:
```
frontend-developer:
  - Create Button.tsx with TypeScript props
  - Implement variants (primary, secondary, danger)
  - Add Tailwind CSS styling
  - Write unit tests with RTL
  - Export from components/index.ts

qa-specialist:
  - Verify accessibility (keyboard, ARIA)
  - Test different variants
  - Check responsive behavior

git-workflow-manager:
  - Commit with proper message
  - Create PR with component demo
```

### Scenario 2: Data-Heavy Feature
**Request**: "Build a user dashboard with charts and real-time updates"

**Domain Detection**: Frontend + Data (keywords: dashboard, charts, real-time)

**Workflow**:
```
spec-manager:
  - Define dashboard requirements
  - Specify data refresh strategy
  - List chart types needed

systems-architect:
  - Design data flow architecture
  - Plan state management approach
  - Define WebSocket integration

frontend-developer:
  - Set up TanStack Query for data
  - Implement chart components (recharts/chart.js)
  - Add WebSocket connection
  - Implement loading/error states
  - Create responsive grid layout

qa-specialist:
  - Test data loading scenarios
  - Verify real-time updates
  - Performance testing

dependency-scanner:
  - Check chart library vulnerabilities
  - Audit WebSocket dependencies
```

### Scenario 3: Performance Optimization
**Request**: "App is slow on initial load, optimize bundle"

**Domain Detection**: Frontend (keywords: slow, optimize, bundle)

**Workflow**:
```
frontend-developer:
  1. Analysis Phase:
     - Run bundle analyzer
     - Profile loading performance
     - Identify large dependencies
     - Check code splitting strategy

  2. Implementation Phase:
     - Implement route-based code splitting
     - Lazy load heavy components
     - Tree-shake unused dependencies
     - Optimize images and assets
     - Add loading skeletons

  3. Verification:
     - Measure FCP, LCP, TTI improvements
     - Test on slow 3G network
     - Verify functionality intact

qa-specialist:
  - Performance regression testing
  - Verify no broken functionality
```

## Anti-Patterns to Avoid

### Common Mistakes
1. **Premature Optimization**: Don't optimize before measuring
2. **Over-Engineering**: KISS - avoid unnecessary abstractions
3. **Prop Drilling**: Use context/state management when appropriate
4. **Ignoring Accessibility**: Build it in from the start
5. **Missing Error Boundaries**: Always handle errors gracefully
6. **Inline Styles Everywhere**: Use proper CSS solution
7. **No Code Splitting**: Don't load everything upfront
8. **Tight Coupling**: Components should be independent

### Technology Over-Use
- Don't use Redux when local state suffices
- Don't add libraries when native solutions exist
- Don't use microservices for simple apps
- Don't over-componentize (too granular)

## Success Metrics

### Development Velocity
- Component creation time < 2 hours
- Feature completion within estimates
- Low bug rate in production

### Code Quality
- ESLint score: 0 errors, 0 warnings
- Type coverage: 100%
- Test coverage: > 80%
- Bundle size: Within budget

### User Experience
- Lighthouse score: > 90
- Core Web Vitals: All green
- Accessibility score: 100
- Zero critical bugs in production

## Resources & References

### Documentation
- [React Docs](https://react.dev)
- [Vue Docs](https://vuejs.org)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [MDN Web Docs](https://developer.mozilla.org)

### Tools
- [Vite](https://vitejs.dev)
- [TanStack Query](https://tanstack.com/query)
- [Tailwind CSS](https://tailwindcss.com)
- [React Testing Library](https://testing-library.com)

### Best Practices
- [Web.dev Patterns](https://web.dev/patterns)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

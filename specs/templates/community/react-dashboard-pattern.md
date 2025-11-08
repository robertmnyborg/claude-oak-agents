# Pattern: React Dashboard Scaffolding

```yaml
pattern_metadata:
  name: "react-dashboard-scaffold"
  category: "frontend"
  difficulty: "beginner"
  tech_stack: ["React", "TypeScript", "React Router", "TanStack Query", "Zustand"]
  tags: ["react", "dashboard", "admin-panel", "typescript", "state-management"]
  version: "1.0.0"
  status: "stable"
  author: "claude-oak-agents"
  last_updated: "2025-11-08"
```

## Problem Statement

### What Challenge Does This Solve?

Creating a production-ready dashboard requires consistent patterns for:
- Layout structure (sidebar, header, content area)
- Data fetching and caching
- Global state management
- Routing and navigation
- Authentication integration
- Responsive design

### When Should You Use This Pattern?

Use this pattern when building:
- ✅ Admin dashboards
- ✅ SaaS application main interface
- ✅ Data visualization dashboards
- ✅ Internal tools

Don't use this pattern when:
- ❌ Simple landing pages
- ❌ Marketing websites
- ❌ Mobile apps (use React Native patterns)

## Solution Overview

### Architecture

```
┌────────────────────────────────────────────┐
│              AppShell                       │
│  ┌──────────┬──────────────────────────┐  │
│  │ Sidebar  │       Header             │  │
│  │          ├──────────────────────────┤  │
│  │  Nav     │                          │  │
│  │  Links   │     Main Content Area    │  │
│  │          │     (React Router        │  │
│  │          │      Outlet)             │  │
│  │          │                          │  │
│  └──────────┴──────────────────────────┘  │
└────────────────────────────────────────────┘

State Management (Zustand)
  ↓
Data Fetching (TanStack Query)
  ↓
API Client (Axios)
```

### Key Design Decisions

1. **React Router v6** - Modern routing with nested layouts
2. **TanStack Query** - Server state caching and synchronization
3. **Zustand** - Lightweight client state (auth, UI preferences)
4. **TypeScript** - Type safety across components

## Technical Design

### Project Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── AppShell.tsx          # Main layout wrapper
│   │   ├── Sidebar.tsx            # Navigation sidebar
│   │   └── Header.tsx             # Top header
│   ├── ui/                        # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Table.tsx
├── pages/
│   ├── Dashboard.tsx              # Dashboard home
│   ├── Projects.tsx               # Projects list
│   └── Settings.tsx               # Settings page
├── hooks/
│   ├── useAuth.ts                 # Authentication hook
│   ├── useProjects.ts             # Projects data hook
│   └── useSettings.ts             # Settings data hook
├── stores/
│   ├── authStore.ts               # Auth state (Zustand)
│   └── uiStore.ts                 # UI preferences (Zustand)
├── api/
│   ├── client.ts                  # Axios instance
│   └── endpoints.ts               # API endpoint definitions
├── types/
│   ├── User.ts
│   ├── Project.ts
│   └── api.ts
└── App.tsx                        # Root component
```

### AppShell Layout

```typescript
// components/layout/AppShell.tsx
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function AppShell() {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <Header />
        
        <main className="flex-1 overflow-y-auto p-6">
          {/* Nested routes render here */}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
```

### Routing Setup

```typescript
// App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppShell from './components/layout/AppShell';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import Settings from './pages/Settings';
import Login from './pages/Login';
import { useAuthStore } from './stores/authStore';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        
        {/* Protected routes with AppShell layout */}
        <Route element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Data Fetching Hook

```typescript
// hooks/useProjects.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api/client';
import type { Project } from '../types/Project';

export function useProjects() {
  return useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const { data } = await api.get<Project[]>('/api/projects');
      return data;
    },
  });
}

export function useCreateProject() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (project: Partial<Project>) => {
      const { data } = await api.post<Project>('/api/projects', project);
      return data;
    },
    onSuccess: () => {
      // Invalidate and refetch projects list
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
}
```

### State Management

```typescript
// stores/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      login: (user) => set({ user, isAuthenticated: true }),
      logout: () => set({ user: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage', // localStorage key
    }
  )
);
```

## Agent Workflow

### Agents Involved
1. **frontend-developer** - React component implementation
2. **qa-specialist** - Component testing
3. **quality-gate** - Code quality validation
4. **git-workflow-manager** - Commit and PR

### Execution Sequence
```
frontend-developer (scaffold dashboard structure)
  ↓
qa-specialist (component and integration tests)
  ↓
quality-gate (validation)
  ↓
git-workflow-manager (commit and PR)
```

## Implementation Checklist

### Phase 1: Project Setup
- [ ] Create React app with TypeScript
- [ ] Install dependencies (react-router-dom, @tanstack/react-query, zustand, axios)
- [ ] Configure TailwindCSS or CSS framework
- [ ] Set up folder structure

### Phase 2: Layout Components
- [ ] Create AppShell component
- [ ] Create Sidebar with navigation
- [ ] Create Header with user menu
- [ ] Style with responsive design

### Phase 3: Routing
- [ ] Set up React Router
- [ ] Define protected routes
- [ ] Implement authentication guards
- [ ] Create page components

### Phase 4: Data Layer
- [ ] Configure TanStack Query client
- [ ] Create API client (Axios)
- [ ] Implement data hooks (useProjects, etc.)
- [ ] Add error handling

### Phase 5: State Management
- [ ] Set up Zustand stores (auth, UI)
- [ ] Implement auth persistence (localStorage)
- [ ] Connect auth to protected routes

### Phase 6: Testing
- [ ] Unit tests for hooks
- [ ] Component tests for UI
- [ ] Integration tests for routing
- [ ] E2E tests for critical flows

## Validation Criteria

### Success Metrics
- [ ] Dashboard loads in <2 seconds
- [ ] Navigation works without page refresh
- [ ] Data fetching with loading states
- [ ] Authentication guards functional
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] TypeScript strict mode passes

## Examples

### Example Dashboard Page

```typescript
// pages/Dashboard.tsx
import { useProjects } from '../hooks/useProjects';
import Card from '../components/ui/Card';

export default function Dashboard() {
  const { data: projects, isLoading, error } = useProjects();
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <h2 className="text-xl font-semibold">Total Projects</h2>
          <p className="text-3xl">{projects?.length}</p>
        </Card>
        
        {/* More stats cards */}
      </div>
      
      {/* Projects table */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Recent Projects</h2>
        <table>
          {/* Table implementation */}
        </table>
      </div>
    </div>
  );
}
```

## Troubleshooting

### Protected Routes Not Working
- Verify useAuthStore returns correct `isAuthenticated` value
- Check auth persistence in localStorage
- Ensure ProtectedRoute wraps AppShell correctly

### Data Not Refetching After Mutation
- Call `queryClient.invalidateQueries()` in mutation `onSuccess`
- Verify queryKey matches between queries and mutations

## References

- [React Router v6 Docs](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query)
- [Zustand](https://github.com/pmndrs/zustand)
- [TypeScript React Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

---

**Pattern Version**: 1.0.0  
**Last Updated**: 2025-11-08  
**Maintained By**: claude-oak-agents community

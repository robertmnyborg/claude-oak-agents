---
template_id: react-dashboard
template_name: React Dashboard Template
category: frontend
difficulty: intermediate
estimated_time: 6-8 hours
tags: [react, typescript, dashboard, tailwind, tanstack-query, vite]
author: claude-oak-agents
version: 1.0.0
last_updated: 2025-11-08
popularity: 90
dependencies: [react, typescript, tailwindcss, tanstack-query, recharts]
related_templates: [rest-crud-api, saas-auth-complete]
---

# React Dashboard Template

Production-ready dashboard application with data tables, charts, responsive layout, and dark mode support.

## Overview

This template provides a complete dashboard implementation featuring:
- Responsive layout with sidebar navigation
- Data tables with sorting, filtering, and pagination (TanStack Table)
- Charts and visualizations (Recharts)
- Dark mode toggle
- API integration with TanStack Query
- TypeScript for type safety
- Tailwind CSS for styling
- Vite for fast development

## Use Cases

- **Admin Panel**: Manage users, content, and settings
- **Analytics Dashboard**: Display metrics and KPIs
- **SaaS Application**: Internal tools and reporting
- **Data Visualization**: Charts, graphs, and tables

## Requirements

### Technical Prerequisites
- Node.js 18+
- React 18+
- TypeScript 5+
- Vite 5+
- Tailwind CSS 3+

### Design Requirements
- Mobile-responsive (works on phones, tablets, desktops)
- Accessible (ARIA labels, keyboard navigation)
- Fast initial load (<2s)
- Dark mode support

## Implementation Plan

### Phase 1: Project Setup (1 hour)

**1.1 Initialize Project**
```bash
npm create vite@latest my-dashboard -- --template react-ts
cd my-dashboard
npm install
```

**1.2 Install Dependencies**
```bash
npm install @tanstack/react-query @tanstack/react-table
npm install recharts lucide-react
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**1.3 Configure Tailwind**
```typescript
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
};
```

**1.4 Project Structure**
```
src/
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── Layout.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Table.tsx
│   └── dashboard/
│       ├── StatsCard.tsx
│       ├── RecentActivity.tsx
│       └── UserTable.tsx
├── hooks/
│   ├── useUsers.ts
│   └── useTheme.ts
├── lib/
│   ├── api.ts
│   └── queryClient.ts
├── pages/
│   ├── Dashboard.tsx
│   ├── Users.tsx
│   └── Settings.tsx
├── types/
│   └── index.ts
├── App.tsx
└── main.tsx
```

### Phase 2: Layout Components (2 hours)

**2.1 Layout Component**
```typescript
// src/components/layout/Layout.tsx
import { ReactNode, useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(true)} />

        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

**2.2 Sidebar Component**
```typescript
// src/components/layout/Sidebar.tsx
import { Home, Users, Settings, X } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Users', href: '/users', icon: Users },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-20 bg-black bg-opacity-50 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
          fixed inset-y-0 left-0 z-30 w-64 bg-white dark:bg-gray-800 transform transition-transform
          lg:static lg:translate-x-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex items-center justify-between p-4">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              Dashboard
            </h1>
            <button onClick={onClose} className="lg:hidden">
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center px-4 py-3 rounded-lg transition-colors
                    ${isActive
                      ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-200'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }
                  `}
                >
                  <item.icon className="mr-3 h-5 w-5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </>
  );
}
```

**2.3 Header Component**
```typescript
// src/components/layout/Header.tsx
import { Menu, Moon, Sun } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';

interface HeaderProps {
  onMenuClick: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 shadow">
      <div className="flex items-center justify-between px-6 py-4">
        <button onClick={onMenuClick} className="lg:hidden">
          <Menu className="h-6 w-6" />
        </button>

        <div className="flex items-center space-x-4">
          <button
            onClick={toggleTheme}
            className="rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            {theme === 'dark' ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
```

### Phase 3: Dashboard Components (2 hours)

**3.1 Stats Cards**
```typescript
// src/components/dashboard/StatsCard.tsx
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  change: string;
  icon: LucideIcon;
  trend: 'up' | 'down';
}

export default function StatsCard({ title, value, change, icon: Icon, trend }: StatsCardProps) {
  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-6 shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
            {title}
          </p>
          <p className="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {value}
          </p>
        </div>
        <div className="rounded-full bg-blue-100 dark:bg-blue-900 p-3">
          <Icon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
        </div>
      </div>
      <div className="mt-4 flex items-center text-sm">
        <span className={trend === 'up' ? 'text-green-600' : 'text-red-600'}>
          {change}
        </span>
        <span className="ml-2 text-gray-600 dark:text-gray-400">vs last month</span>
      </div>
    </div>
  );
}
```

**3.2 User Table**
```typescript
// src/components/dashboard/UserTable.tsx
import { useReactTable, getCoreRowModel, flexRender } from '@tanstack/react-table';
import { User } from '../../types';

interface UserTableProps {
  users: User[];
}

export default function UserTable({ users }: UserTableProps) {
  const columns = [
    {
      accessorKey: 'name',
      header: 'Name',
    },
    {
      accessorKey: 'email',
      header: 'Email',
    },
    {
      accessorKey: 'role',
      header: 'Role',
    },
    {
      accessorKey: 'createdAt',
      header: 'Joined',
      cell: ({ getValue }) => new Date(getValue() as string).toLocaleDateString(),
    },
  ];

  const table = useReactTable({
    data: users,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="overflow-x-auto rounded-lg bg-white dark:bg-gray-800 shadow">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-900">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400"
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td
                  key={cell.id}
                  className="whitespace-nowrap px-6 py-4 text-sm text-gray-900 dark:text-gray-100"
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Phase 4: API Integration (1 hour)

**4.1 TanStack Query Setup**
```typescript
// src/lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});
```

**4.2 API Hooks**
```typescript
// src/hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { User } from '../types';

export function useUsers() {
  return useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await api.get('/users');
      return response.data;
    },
  });
}
```

**4.3 API Client**
```typescript
// src/lib/api.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Phase 5: Dark Mode (1 hour)

**5.1 Theme Hook**
```typescript
// src/hooks/useTheme.ts
import { useEffect, useState } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const stored = localStorage.getItem('theme') as 'light' | 'dark' | null;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    setTheme(stored || (prefersDark ? 'dark' : 'light'));
  }, []);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return { theme, toggleTheme };
}
```

## Agent Workflow

```yaml
agent_sequence:
  phase_1_design:
    - agent: design-simplicity-advisor
      task: "Review dashboard complexity (avoid over-engineering UI)"
      output: "Start simple, add features incrementally"

    - agent: frontend-developer
      task: "Design component structure and layout"
      output: "Component tree, routing, state management plan"

  phase_2_implementation:
    - agent: frontend-developer
      task: "Implement layout components (sidebar, header)"
      duration: "2 hours"

    - agent: frontend-developer
      task: "Implement dashboard components (stats, tables, charts)"
      duration: "2 hours"

    - agent: frontend-developer
      task: "Integrate API with TanStack Query"
      duration: "1 hour"

  phase_3_quality:
    - agent: unit-test-expert
      task: "Component tests with React Testing Library"
      coverage: ">70%"

    - agent: qa-specialist
      task: "Responsive design testing (mobile, tablet, desktop)"

    - agent: quality-gate
      task: "Code review and accessibility check"

  phase_4_deployment:
    - agent: git-workflow-manager
      task: "Create PR with dashboard implementation"
```

## Testing Strategy

### Component Tests
```typescript
import { render, screen } from '@testing-library/react';
import StatsCard from './StatsCard';
import { Users } from 'lucide-react';

test('renders stats card', () => {
  render(
    <StatsCard
      title="Total Users"
      value="1,234"
      change="+12%"
      icon={Users}
      trend="up"
    />
  );

  expect(screen.getByText('Total Users')).toBeInTheDocument();
  expect(screen.getByText('1,234')).toBeInTheDocument();
});
```

### Accessibility Tests
- Keyboard navigation (tab through all interactive elements)
- Screen reader compatibility (ARIA labels)
- Color contrast (WCAG AA compliance)

## Common Pitfalls

### 1. No Loading States
**Problem**: Empty dashboard while fetching data
**Solution**: Show skeletons or spinners during API calls

### 2. Not Mobile-Responsive
**Problem**: Dashboard unusable on mobile
**Solution**: Use Tailwind responsive classes (sm:, md:, lg:)

### 3. Poor Performance
**Problem**: Re-rendering entire table on state change
**Solution**: Use React.memo, useMemo, useCallback appropriately

### 4. No Error Handling
**Problem**: API errors crash the app
**Solution**: TanStack Query error states, error boundaries

### 5. Hardcoded Colors
**Problem**: Dark mode looks broken
**Solution**: Use Tailwind dark: variants consistently

## Success Criteria

- [ ] Responsive layout (mobile, tablet, desktop)
- [ ] Dark mode toggle works
- [ ] Data tables with sorting and pagination
- [ ] Charts display correctly
- [ ] API integration with loading/error states
- [ ] Accessibility (keyboard navigation, ARIA labels)
- [ ] Fast initial load (<2s)
- [ ] Test coverage >70%

## Performance Optimization

- Code splitting (React.lazy for routes)
- Image optimization (WebP, lazy loading)
- Bundle size analysis (vite-plugin-bundle-analyzer)
- Memoization for expensive computations
- Virtual scrolling for large tables (TanStack Virtual)

## Future Enhancements

- Advanced filtering and search
- Data export (CSV, PDF)
- Real-time updates (WebSocket)
- Customizable dashboard widgets
- Multi-language support (i18n)

---
name: vite-csr
description: Vite-based React SPA patterns. Activated when working with React Router, code splitting, client-side state management, or Vite configuration.
---

# Vite CSR Project

> Vite-based React SPA/CSR project patterns

## Project Structure (FSD)

```
src/
├── app/                      # App Layer
│   ├── providers/            # Context Providers
│   ├── router/               # React Router config
│   ├── styles/               # Global styles
│   └── index.tsx             # App Entry
├── pages/                    # Pages Layer
│   ├── home/
│   ├── dashboard/
│   └── settings/
├── widgets/
├── features/
├── entities/
├── shared/
│   ├── api/
│   ├── config/
│   ├── lib/
│   └── ui/
├── main.tsx                  # Entry Point
└── vite-env.d.ts
```

## Core Patterns

### 1. App Providers

```typescript
// app/providers/index.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { HelmetProvider } from 'react-helmet-async';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <HelmetProvider>
        <QueryClientProvider client={queryClient}>
          <Suspense fallback={<GlobalSpinner />}>
            {children}
          </Suspense>
          <ReactQueryDevtools initialIsOpen={false} />
        </QueryClientProvider>
      </HelmetProvider>
    </ErrorBoundary>
  );
}
```

### 2. React Router

```typescript
// app/router/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const HomePage = lazy(() => import('@/pages/home'));
const DashboardPage = lazy(() => import('@/pages/dashboard'));
const SettingsPage = lazy(() => import('@/pages/settings'));

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: (
          <Suspense fallback={<PageSkeleton />}>
            <HomePage />
          </Suspense>
        ),
      },
      {
        path: 'dashboard',
        element: (
          <Suspense fallback={<PageSkeleton />}>
            <DashboardPage />
          </Suspense>
        ),
      },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
```

### 3. Protected Routes

```typescript
// app/router/protected-route.tsx
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '@/features/auth';

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}
```

### 4. Page Component

```typescript
// pages/dashboard/index.tsx
import { Helmet } from 'react-helmet-async';
import { DashboardStats } from '@/widgets/dashboard-stats';
import { RecentActivity } from '@/widgets/recent-activity';

export default function DashboardPage() {
  return (
    <>
      <Helmet>
        <title>Dashboard | MyApp</title>
        <meta name="description" content="View your dashboard" />
      </Helmet>
      <main className="dashboard-page">
        <h1>Dashboard</h1>
        <DashboardStats />
        <RecentActivity />
      </main>
    </>
  );
}
```

### 5. API Client

```typescript
// shared/api/client.ts
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### 6. Environment Variables

```typescript
// vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
  readonly VITE_SENTRY_DSN: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

```typescript
// shared/config/env.ts
export const env = {
  apiUrl: import.meta.env.VITE_API_URL,
  appTitle: import.meta.env.VITE_APP_TITLE,
  sentryDsn: import.meta.env.VITE_SENTRY_DSN,
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
} as const;
```

### 7. Authentication (Zustand)

```typescript
// features/auth/model/store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
      login: (user, accessToken) => set({ user, accessToken, isAuthenticated: true }),
      logout: () => set({ user: null, accessToken: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
```

### 8. SEO (React Helmet)

```typescript
// shared/ui/seo/index.tsx
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description?: string;
  image?: string;
  url?: string;
}

export function SEO({ title, description, image, url }: SEOProps) {
  const siteTitle = import.meta.env.VITE_APP_TITLE;
  const fullTitle = `${title} | ${siteTitle}`;

  return (
    <Helmet>
      <title>{fullTitle}</title>
      {description && <meta name="description" content={description} />}
      <meta property="og:title" content={fullTitle} />
      {description && <meta property="og:description" content={description} />}
      {image && <meta property="og:image" content={image} />}
      {url && <meta property="og:url" content={url} />}
    </Helmet>
  );
}
```

## Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          query: ['@tanstack/react-query'],
        },
      },
    },
    sourcemap: true,
  },
});
```

## Code Splitting

```typescript
// Route-level
const Dashboard = lazy(() => import('@/pages/dashboard'));

// Component-level
const HeavyChart = lazy(() => import('@/widgets/heavy-chart'));

// Named export
const AdminPanel = lazy(() =>
  import('@/widgets/admin-panel').then((module) => ({
    default: module.AdminPanel,
  }))
);

// Prefetch on hover
const prefetchDashboard = () => { import('@/pages/dashboard'); };
<Link to="/dashboard" onMouseEnter={prefetchDashboard}>Dashboard</Link>
```

## Best Practices

|Practice|Description|
|---|---|
|Lazy Loading|Always lazy import page components|
|Error Boundaries|Per-route error handling|
|Code Splitting|manualChunks for vendor bundle separation|
|Env vars|VITE_ prefix for client env vars|
|SEO|react-helmet-async for meta tags|
|Type safety|vite-env.d.ts for env var types|

## DO NOT

```typescript
// AVOID: synchronous import (increases bundle size)
import Dashboard from '@/pages/dashboard';

// AVOID: wrong env var access
const apiUrl = process.env.REACT_APP_API_URL; // doesn't work in Vite

// AVOID: auth state via props drilling
<App isAuthenticated={isAuth} user={user} />

// AVOID: missing SEO
export default function Page() {
  return <div>Content</div>; // no title, no description
}
```

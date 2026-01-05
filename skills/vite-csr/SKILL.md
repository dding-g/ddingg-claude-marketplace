# Vite CSR Project Skill

> Vite 기반 React SPA/CSR 프로젝트 개발 가이드

## Overview

Vite를 빌드 도구로 사용하는 클라이언트 사이드 렌더링(CSR) React 프로젝트의 패턴과 베스트 프랙티스를 제공합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- Vite, CSR, SPA 언급
- React Router 라우팅 관련
- 클라이언트 사이드 상태 관리
- 번들 최적화, 코드 스플리팅 관련

## Project Structure (FSD)

```
src/
├── app/                      # App Layer
│   ├── providers/            # Context Providers
│   ├── router/               # React Router 설정
│   ├── styles/               # 글로벌 스타일
│   └── index.tsx             # App Entry
├── pages/                    # Pages Layer
│   ├── home/
│   ├── dashboard/
│   └── settings/
├── widgets/                  # Widgets Layer
├── features/                 # Features Layer
├── entities/                 # Entities Layer
├── shared/                   # Shared Layer
│   ├── api/
│   ├── config/
│   ├── lib/
│   └── ui/
├── main.tsx                  # Entry Point
└── vite-env.d.ts
```

## Core Patterns

### 1. App Providers Setup

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

### 2. React Router Setup

```typescript
// app/router/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { lazy, Suspense } from 'react';

// Lazy Loading
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
      {
        path: 'settings',
        element: (
          <Suspense fallback={<PageSkeleton />}>
            <SettingsPage />
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

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}

// Router에서 사용
const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <HomePage /> },
      {
        element: <ProtectedRoute />,
        children: [
          { path: 'dashboard', element: <DashboardPage /> },
          { path: 'settings', element: <SettingsPage /> },
        ],
      },
    ],
  },
]);
```

### 4. Page Component Pattern

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

### 5. API Client Setup

```typescript
// shared/api/client.ts
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
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

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // 토큰 갱신 또는 로그아웃 처리
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

### 7. Authentication Pattern

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

      login: (user, accessToken) => {
        set({ user, accessToken, isAuthenticated: true });
      },

      logout: () => {
        set({ user: null, accessToken: null, isAuthenticated: false });
      },
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

### 8. SEO with React Helmet

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

      {/* Open Graph */}
      <meta property="og:title" content={fullTitle} />
      {description && <meta property="og:description" content={description} />}
      {image && <meta property="og:image" content={image} />}
      {url && <meta property="og:url" content={url} />}

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      {description && <meta name="twitter:description" content={description} />}
      {image && <meta name="twitter:image" content={image} />}
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
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
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

## Performance Optimization

### Code Splitting

```typescript
// 라우트 레벨 코드 스플리팅
const Dashboard = lazy(() => import('@/pages/dashboard'));

// 컴포넌트 레벨 코드 스플리팅
const HeavyChart = lazy(() => import('@/widgets/heavy-chart'));

// 조건부 로딩
const AdminPanel = lazy(() =>
  import('@/widgets/admin-panel').then((module) => ({
    default: module.AdminPanel,
  }))
);
```

### Prefetching

```typescript
// 마우스 호버 시 프리페치
const prefetchDashboard = () => {
  import('@/pages/dashboard');
};

<Link to="/dashboard" onMouseEnter={prefetchDashboard}>
  Dashboard
</Link>
```

## Best Practices

1. **Lazy Loading**: 페이지 컴포넌트는 항상 lazy import
2. **Error Boundaries**: 라우트별 에러 처리
3. **Code Splitting**: manualChunks로 벤더 번들 분리
4. **환경 변수**: VITE_ 접두사로 클라이언트 환경 변수 관리
5. **SEO**: react-helmet-async로 메타 태그 관리
6. **타입 안전성**: vite-env.d.ts로 환경 변수 타입 정의

## Anti-Patterns

```typescript
// ❌ 동기 import로 번들 크기 증가
import Dashboard from '@/pages/dashboard';

// ❌ 환경 변수 직접 접근
const apiUrl = process.env.REACT_APP_API_URL; // Vite에서 동작 안 함

// ❌ 인증 상태를 props로 전달
<App isAuthenticated={isAuth} user={user} /> // Props Drilling

// ❌ SEO 미적용
export default function Page() {
  return <div>Content</div>; // 제목, 설명 없음
}
```

# Vite CSR Routing Patterns

## React Router v6 Setup

### Basic Configuration

```typescript
// app/router/routes.tsx
import { RouteObject } from 'react-router-dom';
import { lazy, Suspense } from 'react';

// Lazy imports
const HomePage = lazy(() => import('@/pages/home'));
const AboutPage = lazy(() => import('@/pages/about'));
const NotFoundPage = lazy(() => import('@/pages/not-found'));

// Layout
import { RootLayout } from '@/widgets/layout';
import { PageSkeleton } from '@/shared/ui/skeleton';

const withSuspense = (Component: React.LazyExoticComponent<any>) => (
  <Suspense fallback={<PageSkeleton />}>
    <Component />
  </Suspense>
);

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: withSuspense(HomePage) },
      { path: 'about', element: withSuspense(AboutPage) },
      { path: '*', element: withSuspense(NotFoundPage) },
    ],
  },
];
```

## Route Guards

### Authentication Guard

```typescript
// app/router/guards/auth-guard.tsx
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/features/auth';

export function AuthGuard() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}
```

### Role-Based Guard

```typescript
// app/router/guards/role-guard.tsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/features/auth';

interface RoleGuardProps {
  allowedRoles: string[];
}

export function RoleGuard({ allowedRoles }: RoleGuardProps) {
  const user = useAuthStore((s) => s.user);

  if (!user || !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
}

// 사용 예시
const routes: RouteObject[] = [
  {
    element: <AuthGuard />,
    children: [
      {
        element: <RoleGuard allowedRoles={['admin']} />,
        children: [
          { path: 'admin', element: <AdminPage /> },
        ],
      },
    ],
  },
];
```

## Dynamic Routes

```typescript
// pages/users/[id]/index.tsx
import { useParams } from 'react-router-dom';
import { useUser } from '@/entities/user';

export default function UserDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: user, isLoading } = useUser(id!);

  if (isLoading) return <UserSkeleton />;
  if (!user) return <NotFound />;

  return <UserProfile user={user} />;
}

// Route 정의
{ path: 'users/:id', element: withSuspense(UserDetailPage) }
```

## Nested Routes

```typescript
const routes: RouteObject[] = [
  {
    path: '/dashboard',
    element: <DashboardLayout />,
    children: [
      { index: true, element: <DashboardOverview /> },
      { path: 'analytics', element: <AnalyticsPage /> },
      {
        path: 'settings',
        element: <SettingsLayout />,
        children: [
          { index: true, element: <GeneralSettings /> },
          { path: 'profile', element: <ProfileSettings /> },
          { path: 'security', element: <SecuritySettings /> },
        ],
      },
    ],
  },
];
```

## Navigation Hooks

```typescript
// shared/lib/navigation.ts
import { useNavigate, useLocation, useSearchParams } from 'react-router-dom';

// 프로그래매틱 네비게이션
export function useAppNavigate() {
  const navigate = useNavigate();

  return {
    goHome: () => navigate('/'),
    goBack: () => navigate(-1),
    goTo: (path: string) => navigate(path),
    replace: (path: string) => navigate(path, { replace: true }),
  };
}

// 쿼리 파라미터 관리
export function useQueryParams<T extends Record<string, string>>() {
  const [searchParams, setSearchParams] = useSearchParams();

  const params = Object.fromEntries(searchParams.entries()) as T;

  const setParams = (newParams: Partial<T>) => {
    setSearchParams((prev) => {
      Object.entries(newParams).forEach(([key, value]) => {
        if (value === undefined || value === null || value === '') {
          prev.delete(key);
        } else {
          prev.set(key, value);
        }
      });
      return prev;
    });
  };

  return { params, setParams };
}
```

## Route-Based Data Loading

```typescript
// React Router v6.4+ Data API
import { createBrowserRouter } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/users/:id',
    element: <UserDetailPage />,
    loader: async ({ params }) => {
      const user = await fetchUser(params.id!);
      return { user };
    },
    errorElement: <ErrorPage />,
  },
]);

// 컴포넌트에서 사용
import { useLoaderData } from 'react-router-dom';

function UserDetailPage() {
  const { user } = useLoaderData() as { user: User };
  return <UserProfile user={user} />;
}
```

## Scroll Restoration

```typescript
// app/router/scroll-restoration.tsx
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

// RootLayout에서 사용
function RootLayout() {
  return (
    <>
      <ScrollToTop />
      <Header />
      <Outlet />
      <Footer />
    </>
  );
}
```

## Route Transition Animation

```typescript
// shared/ui/page-transition.tsx
import { motion, AnimatePresence } from 'framer-motion';
import { useLocation, Outlet } from 'react-router-dom';

export function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        <Outlet />
      </motion.div>
    </AnimatePresence>
  );
}
```

## Best Practices

1. **Lazy Loading**: 모든 페이지 컴포넌트는 lazy import
2. **Guard Composition**: 작은 단위의 가드를 조합하여 사용
3. **Type Safety**: useParams에 제네릭으로 타입 지정
4. **Error Handling**: 라우트별 errorElement 설정
5. **URL State**: 필터, 페이지네이션은 URL로 관리

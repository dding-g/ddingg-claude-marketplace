# React Native Navigation Patterns

## Expo Router Setup

### File-Based Routing

```
app/
├── _layout.tsx           # Root Layout
├── index.tsx             # / (Home)
├── +not-found.tsx        # 404 Page
├── (auth)/               # Auth Group (not in URL)
│   ├── _layout.tsx
│   ├── login.tsx         # /login
│   └── signup.tsx        # /signup
├── (tabs)/               # Tab Navigator
│   ├── _layout.tsx
│   ├── index.tsx         # / (Home Tab)
│   ├── search.tsx        # /search
│   └── profile.tsx       # /profile
├── products/
│   ├── index.tsx         # /products
│   └── [id].tsx          # /products/:id
└── settings/
    ├── _layout.tsx       # Stack for settings
    ├── index.tsx         # /settings
    └── notifications.tsx # /settings/notifications
```

## Root Layout

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';
import { useAuth } from '@/features/auth';

export default function RootLayout() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      {!isAuthenticated ? (
        <Stack.Screen name="(auth)" />
      ) : (
        <>
          <Stack.Screen name="(tabs)" />
          <Stack.Screen
            name="products/[id]"
            options={{
              presentation: 'card',
              headerShown: true,
              headerTitle: 'Product Detail',
            }}
          />
        </>
      )}
    </Stack>
  );
}
```

## Tab Navigation

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { TabBarIcon } from '@/shared/ui/tab-bar-icon';
import { useTheme } from '@/shared/lib/theme';

export default function TabLayout() {
  const { colors } = useTheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.gray,
        tabBarStyle: {
          backgroundColor: colors.background,
          borderTopColor: colors.border,
        },
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="search"
        options={{
          title: 'Search',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'search' : 'search-outline'} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'person' : 'person-outline'} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
```

## Dynamic Routes

```typescript
// app/products/[id].tsx
import { Stack, useLocalSearchParams, useRouter } from 'expo-router';
import { useProduct } from '@/entities/product';

export default function ProductDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { data: product, isLoading } = useProduct(id);

  if (isLoading) return <ProductDetailSkeleton />;
  if (!product) {
    return (
      <>
        <Stack.Screen options={{ title: 'Not Found' }} />
        <NotFoundView onGoBack={() => router.back()} />
      </>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: product.name,
          headerRight: () => <ShareButton product={product} />,
        }}
      />
      <ProductDetail product={product} />
    </>
  );
}
```

## Programmatic Navigation

```typescript
import { router, useRouter, Href } from 'expo-router';

// 전역 네비게이션
function goToProduct(id: string) {
  router.push(`/products/${id}`);
}

// 컴포넌트 내 네비게이션
function ProductCard({ product }: Props) {
  const router = useRouter();

  const handlePress = () => {
    router.push({
      pathname: '/products/[id]',
      params: { id: product.id },
    });
  };

  return (
    <Pressable onPress={handlePress}>
      <Text>{product.name}</Text>
    </Pressable>
  );
}

// Navigation Methods
router.push('/path');           // Stack에 추가
router.replace('/path');        // 현재 화면 교체
router.back();                  // 뒤로 가기
router.canGoBack();             // 뒤로 갈 수 있는지
router.dismissAll();            // 모든 모달 닫기
router.setParams({ key: 'val' }); // 파라미터 업데이트
```

## Modal Navigation

```typescript
// app/_layout.tsx
export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen
        name="modal"
        options={{
          presentation: 'modal',
          headerShown: false,
        }}
      />
      <Stack.Screen
        name="fullscreen-modal"
        options={{
          presentation: 'fullScreenModal',
          headerShown: true,
          headerTitle: 'Full Screen',
        }}
      />
    </Stack>
  );
}

// 모달 열기
router.push('/modal');
```

## Deep Linking

```typescript
// app.json
{
  "expo": {
    "scheme": "myapp",
    "web": {
      "bundler": "metro"
    }
  }
}

// Deep Link 처리
// myapp://products/123 → /products/123

import { useURL } from 'expo-linking';
import { useEffect } from 'react';

export function DeepLinkHandler() {
  const url = useURL();

  useEffect(() => {
    if (url) {
      // URL 파싱 및 네비게이션
      const path = parseDeepLink(url);
      router.push(path);
    }
  }, [url]);

  return null;
}
```

## Protected Routes

```typescript
// app/(protected)/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/features/auth';

export default function ProtectedLayout() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Redirect href="/login" />;
  }

  return (
    <Stack>
      <Stack.Screen name="dashboard" />
      <Stack.Screen name="settings" />
    </Stack>
  );
}
```

## Nested Stack in Tabs

```typescript
// app/(tabs)/profile/_layout.tsx
import { Stack } from 'expo-router';

export default function ProfileLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{ headerTitle: 'Profile' }}
      />
      <Stack.Screen
        name="edit"
        options={{ headerTitle: 'Edit Profile' }}
      />
      <Stack.Screen
        name="orders"
        options={{ headerTitle: 'Order History' }}
      />
    </Stack>
  );
}
```

## Navigation Guards

```typescript
// shared/lib/hooks/use-navigation-guard.ts
import { useRouter, useSegments, useRootNavigationState } from 'expo-router';
import { useEffect } from 'react';
import { useAuth } from '@/features/auth';

export function useNavigationGuard() {
  const { isAuthenticated, isLoading } = useAuth();
  const segments = useSegments();
  const router = useRouter();
  const navigationState = useRootNavigationState();

  useEffect(() => {
    if (!navigationState?.key || isLoading) return;

    const inAuthGroup = segments[0] === '(auth)';

    if (!isAuthenticated && !inAuthGroup) {
      router.replace('/login');
    } else if (isAuthenticated && inAuthGroup) {
      router.replace('/');
    }
  }, [isAuthenticated, segments, isLoading, navigationState?.key]);
}
```

## Custom Transitions

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        animation: 'slide_from_right',
        gestureEnabled: true,
        gestureDirection: 'horizontal',
      }}
    >
      <Stack.Screen name="(tabs)" />
      <Stack.Screen
        name="details"
        options={{
          animation: 'fade_from_bottom',
        }}
      />
    </Stack>
  );
}
```

## Best Practices

1. **File-Based Routing**: Expo Router의 파일 기반 라우팅 활용
2. **Route Groups**: (auth), (tabs) 등으로 논리적 그룹화
3. **Type-Safe Params**: useLocalSearchParams에 제네릭 사용
4. **Loading States**: 인증 확인 중 SplashScreen 표시
5. **Deep Links**: 앱 스킴 설정으로 딥링크 지원
6. **Screen Options**: Stack.Screen에서 동적으로 헤더 설정

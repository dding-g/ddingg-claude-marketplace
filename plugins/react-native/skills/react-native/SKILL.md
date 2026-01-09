---
name: react-native
description: React Native/Expo 모바일 앱 개발 패턴. Expo Router, 네이티브 기능, 성능 최적화 관련 코드 작성 시 활성화됩니다.
---

# React Native Skill

> React Native / Expo 기반 모바일 앱 개발 가이드

## Overview

React Native와 Expo를 사용한 크로스 플랫폼 모바일 앱 개발의 패턴과 베스트 프랙티스를 제공합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- React Native, Expo 언급
- 모바일 앱 개발 관련
- 네비게이션, 네이티브 모듈 관련
- iOS, Android 플랫폼 관련

## Project Structure (FSD + Expo Router)

```
src/
├── app/                      # Expo Router (File-based routing)
│   ├── (auth)/               # Auth Group
│   │   ├── login.tsx
│   │   └── signup.tsx
│   ├── (tabs)/               # Tab Navigation
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   ├── explore.tsx
│   │   └── profile.tsx
│   ├── _layout.tsx           # Root Layout
│   └── +not-found.tsx
├── entities/
├── features/
├── shared/
│   ├── api/
│   ├── config/
│   ├── lib/
│   └── ui/
├── widgets/
└── assets/
```

## Core Patterns

### 1. Expo Router Layout

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <QueryClientProvider client={queryClient}>
          <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="(auth)" />
            <Stack.Screen name="(tabs)" />
          </Stack>
        </QueryClientProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
```

### 2. Tab Navigation

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: 'Explore',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="compass" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
```

### 3. Stack Navigation with Params

```typescript
// app/users/[id].tsx
import { useLocalSearchParams } from 'expo-router';
import { useUser } from '@/entities/user';

export default function UserDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data: user, isLoading } = useUser(id);

  if (isLoading) return <LoadingScreen />;
  if (!user) return <NotFoundScreen />;

  return <UserProfile user={user} />;
}

// 네비게이션
import { router } from 'expo-router';

// Push
router.push(`/users/${userId}`);

// Replace
router.replace('/login');

// Back
router.back();
```

### 4. Authentication Flow

```typescript
// app/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/features/auth';

export default function RootLayout() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <Stack.Screen name="(tabs)" />
      ) : (
        <Stack.Screen name="(auth)" />
      )}
    </Stack>
  );
}
```

### 5. Secure Storage

```typescript
// shared/lib/storage.ts
import * as SecureStore from 'expo-secure-store';

export const secureStorage = {
  async getItem(key: string): Promise<string | null> {
    return SecureStore.getItemAsync(key);
  },

  async setItem(key: string, value: string): Promise<void> {
    await SecureStore.setItemAsync(key, value);
  },

  async removeItem(key: string): Promise<void> {
    await SecureStore.deleteItemAsync(key);
  },
};

// Zustand persist와 함께 사용
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => secureStorage),
    }
  )
);
```

### 6. Platform-Specific Code

```typescript
// shared/ui/button/index.tsx
import { Platform, Pressable, StyleSheet } from 'react-native';

export function Button({ onPress, children, ...props }: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        Platform.select({
          ios: pressed && styles.iosPressed,
          android: {}, // Ripple 효과 사용
        }),
      ]}
      android_ripple={{ color: 'rgba(0,0,0,0.1)' }}
      {...props}
    >
      {children}
    </Pressable>
  );
}

// 플랫폼별 파일 분리
// shared/ui/date-picker/index.ios.tsx
// shared/ui/date-picker/index.android.tsx
```

### 7. Safe Area Handling

```typescript
// shared/ui/screen/index.tsx
import { View, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface ScreenProps {
  children: React.ReactNode;
  edges?: ('top' | 'bottom' | 'left' | 'right')[];
}

export function Screen({ children, edges = ['top'] }: ScreenProps) {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={[
        styles.container,
        {
          paddingTop: edges.includes('top') ? insets.top : 0,
          paddingBottom: edges.includes('bottom') ? insets.bottom : 0,
          paddingLeft: edges.includes('left') ? insets.left : 0,
          paddingRight: edges.includes('right') ? insets.right : 0,
        },
      ]}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
```

### 8. Keyboard Handling

```typescript
// shared/ui/keyboard-avoiding-view/index.tsx
import {
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  TouchableWithoutFeedback,
  Keyboard,
} from 'react-native';

interface Props {
  children: React.ReactNode;
}

export function KeyboardDismissView({ children }: Props) {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        {children}
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
```

### 9. Network Status

```typescript
// shared/lib/hooks/use-network.ts
import NetInfo from '@react-native-community/netinfo';
import { useEffect, useState } from 'react';

export function useNetwork() {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state) => {
      setIsConnected(state.isConnected ?? true);
    });

    return () => unsubscribe();
  }, []);

  return { isConnected };
}

// Offline Banner
export function OfflineBanner() {
  const { isConnected } = useNetwork();

  if (isConnected) return null;

  return (
    <View style={styles.banner}>
      <Text style={styles.text}>오프라인 상태입니다</Text>
    </View>
  );
}
```

### 10. Push Notifications

```typescript
// features/notifications/lib/push.ts
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export async function registerForPushNotifications() {
  if (!Device.isDevice) {
    console.log('Push notifications require a physical device');
    return null;
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    return null;
  }

  const token = await Notifications.getExpoPushTokenAsync();

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
    });
  }

  return token.data;
}
```

## Styling Patterns

### NativeWind (Tailwind for RN)

```typescript
// shared/ui/card/index.tsx
import { View, Text } from 'react-native';

export function Card({ title, children }: CardProps) {
  return (
    <View className="bg-white rounded-xl p-4 shadow-sm">
      <Text className="text-lg font-semibold text-gray-900">
        {title}
      </Text>
      {children}
    </View>
  );
}
```

### StyleSheet Pattern

```typescript
// shared/ui/card/index.tsx
import { View, Text, StyleSheet } from 'react-native';

export function Card({ title, children }: CardProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3, // Android
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111',
  },
});
```

## Performance Optimization

### FlashList (FlatList 대안)

```typescript
import { FlashList } from '@shopify/flash-list';

function ProductList({ products }: { products: Product[] }) {
  return (
    <FlashList
      data={products}
      renderItem={({ item }) => <ProductCard product={item} />}
      estimatedItemSize={100}
      keyExtractor={(item) => item.id}
    />
  );
}
```

### Image Optimization

```typescript
import { Image } from 'expo-image';

function Avatar({ uri }: { uri: string }) {
  return (
    <Image
      source={uri}
      style={{ width: 50, height: 50, borderRadius: 25 }}
      placeholder={blurhash}
      contentFit="cover"
      transition={200}
    />
  );
}
```

### Memoization

```typescript
import { memo, useCallback } from 'react';

const ProductCard = memo(function ProductCard({ product, onPress }: Props) {
  return (
    <Pressable onPress={() => onPress(product.id)}>
      <Text>{product.name}</Text>
    </Pressable>
  );
});

function ProductList({ products }: Props) {
  const handlePress = useCallback((id: string) => {
    router.push(`/products/${id}`);
  }, []);

  return (
    <FlashList
      data={products}
      renderItem={({ item }) => (
        <ProductCard product={item} onPress={handlePress} />
      )}
      estimatedItemSize={100}
    />
  );
}
```

## Best Practices

1. **Expo Router**: File-based routing으로 네비게이션 구성
2. **Safe Area**: 항상 SafeAreaProvider와 useSafeAreaInsets 사용
3. **SecureStore**: 민감한 정보는 SecureStore에 저장
4. **FlashList**: 대용량 리스트는 FlashList 사용
5. **expo-image**: 이미지 최적화를 위해 expo-image 사용
6. **Platform.select**: 플랫폼별 스타일/동작 분기
7. **Gesture Handler**: 복잡한 제스처는 react-native-gesture-handler 사용

## Anti-Patterns

```typescript
// ❌ 인라인 스타일 남용
<View style={{ flex: 1, padding: 16, backgroundColor: '#fff' }} />

// ❌ FlatList 대신 map 사용
{items.map(item => <Item key={item.id} />)}

// ❌ 이미지 크기 미지정
<Image source={{ uri }} /> // width, height 필수

// ❌ 민감한 정보를 AsyncStorage에 저장
await AsyncStorage.setItem('token', token); // SecureStore 사용

// ❌ 키보드 회피 처리 누락
<TextInput /> // KeyboardAvoidingView로 감싸기
```

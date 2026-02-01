---
name: react-native
description: React Native/Expo mobile app patterns. Activated when working with Expo Router, native features, performance optimization, or mobile-specific code.
---

# React Native

> React Native / Expo mobile app development patterns

## Project Structure (FSD + Expo Router)

```
src/
├── app/                      # Expo Router (File-based routing)
│   ├── (auth)/
│   │   ├── login.tsx
│   │   └── signup.tsx
│   ├── (tabs)/
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

### 1. Root Layout

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
    <Tabs screenOptions={{ tabBarActiveTintColor: '#007AFF', headerShown: false }}>
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

// Navigation
import { router } from 'expo-router';
router.push(`/users/${userId}`);
router.replace('/login');
router.back();
```

### 4. Authentication Flow

```typescript
// app/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/features/auth';

export default function RootLayout() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <SplashScreen />;

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

// Zustand persist with SecureStore
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
          android: {},
        }),
      ]}
      android_ripple={{ color: 'rgba(0,0,0,0.1)' }}
      {...props}
    >
      {children}
    </Pressable>
  );
}

// Platform-specific file split
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
        },
      ]}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
});
```

### 8. Keyboard Handling

```typescript
import {
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard,
} from 'react-native';

export function KeyboardDismissView({ children }: { children: React.ReactNode }) {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ flex: 1 }}
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        {children}
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
}
```

### 9. Push Notifications

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
  if (!Device.isDevice) return null;

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') return null;

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

## Styling

### NativeWind (Tailwind for RN)

```typescript
export function Card({ title, children }: CardProps) {
  return (
    <View className="bg-white rounded-xl p-4 shadow-sm">
      <Text className="text-lg font-semibold text-gray-900">{title}</Text>
      {children}
    </View>
  );
}
```

### StyleSheet

```typescript
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
    elevation: 3,
  },
  title: { fontSize: 18, fontWeight: '600', color: '#111' },
});
```

## Performance

```typescript
// FlashList for large lists
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={products}
  renderItem={({ item }) => <ProductCard product={item} />}
  estimatedItemSize={100}
  keyExtractor={(item) => item.id}
/>

// expo-image for optimized images
import { Image } from 'expo-image';

<Image
  source={uri}
  style={{ width: 50, height: 50, borderRadius: 25 }}
  placeholder={blurhash}
  contentFit="cover"
  transition={200}
/>

// Memoization for list items
const ProductCard = memo(function ProductCard({ product, onPress }: Props) {
  return (
    <Pressable onPress={() => onPress(product.id)}>
      <Text>{product.name}</Text>
    </Pressable>
  );
});
```

## Best Practices

|Practice|Description|
|---|---|
|Expo Router|File-based routing for navigation|
|Safe Area|Always use SafeAreaProvider + useSafeAreaInsets|
|SecureStore|Store sensitive data in SecureStore|
|FlashList|Use for large lists instead of FlatList|
|expo-image|Use for optimized image loading|
|Platform.select|Branch per-platform styles/behavior|

## DO NOT

```typescript
// AVOID: inline styles overuse
<View style={{ flex: 1, padding: 16, backgroundColor: '#fff' }} />

// AVOID: map instead of FlatList/FlashList for lists
{items.map(item => <Item key={item.id} />)}

// AVOID: missing image dimensions
<Image source={{ uri }} /> // width, height required

// AVOID: sensitive data in AsyncStorage
await AsyncStorage.setItem('token', token); // use SecureStore

// AVOID: missing keyboard avoidance
<TextInput /> // wrap with KeyboardAvoidingView
```

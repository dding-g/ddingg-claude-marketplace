# React Native Performance Patterns

## List Optimization

### FlashList (Recommended)

```typescript
import { FlashList } from '@shopify/flash-list';

function ProductList({ products }: { products: Product[] }) {
  return (
    <FlashList
      data={products}
      renderItem={({ item }) => <ProductCard product={item} />}
      estimatedItemSize={120} // 예상 아이템 높이
      keyExtractor={(item) => item.id}
      // 추가 최적화 옵션
      drawDistance={250} // 미리 렌더링할 거리
      overrideItemLayout={(layout, item, index) => {
        // 다양한 높이의 아이템
        layout.size = item.hasImage ? 200 : 100;
      }}
    />
  );
}
```

### Memoized Item Component

```typescript
import { memo, useCallback } from 'react';

interface ProductCardProps {
  product: Product;
  onPress: (id: string) => void;
}

// memo로 불필요한 리렌더링 방지
const ProductCard = memo(function ProductCard({
  product,
  onPress,
}: ProductCardProps) {
  const handlePress = useCallback(() => {
    onPress(product.id);
  }, [product.id, onPress]);

  return (
    <Pressable onPress={handlePress}>
      <Image source={{ uri: product.image }} style={styles.image} />
      <Text>{product.name}</Text>
      <Text>{product.price}</Text>
    </Pressable>
  );
});

function ProductList({ products }: Props) {
  // useCallback으로 함수 참조 안정화
  const handleProductPress = useCallback((id: string) => {
    router.push(`/products/${id}`);
  }, []);

  return (
    <FlashList
      data={products}
      renderItem={({ item }) => (
        <ProductCard product={item} onPress={handleProductPress} />
      )}
      estimatedItemSize={120}
    />
  );
}
```

## Image Optimization

### expo-image

```typescript
import { Image } from 'expo-image';

// 블러해시 placeholder
const blurhash = 'L6PZfSi_.AyE_3t7t7R**0o#DgR4';

function OptimizedImage({ uri, width, height }: Props) {
  return (
    <Image
      source={uri}
      placeholder={blurhash}
      contentFit="cover"
      transition={200}
      style={{ width, height }}
      // 메모리 최적화
      recyclingKey={uri}
      cachePolicy="memory-disk"
    />
  );
}
```

### 이미지 프리로딩

```typescript
import { Image } from 'expo-image';

// 앱 시작 시 중요 이미지 프리로드
async function prefetchImages(urls: string[]) {
  await Promise.all(urls.map((url) => Image.prefetch(url)));
}

// 사용
useEffect(() => {
  const criticalImages = [
    '/assets/logo.png',
    '/assets/hero-banner.jpg',
  ];
  prefetchImages(criticalImages);
}, []);
```

## Animation Performance

### Reanimated (UI Thread)

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';

function AnimatedCard() {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  const handlePressIn = () => {
    scale.value = withSpring(0.95);
    opacity.value = withTiming(0.8, { duration: 100 });
  };

  const handlePressOut = () => {
    scale.value = withSpring(1);
    opacity.value = withTiming(1, { duration: 100 });
  };

  return (
    <Pressable onPressIn={handlePressIn} onPressOut={handlePressOut}>
      <Animated.View style={[styles.card, animatedStyle]}>
        <Text>Animated Card</Text>
      </Animated.View>
    </Pressable>
  );
}
```

### Gesture Handler

```typescript
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  runOnJS,
} from 'react-native-reanimated';

function SwipeableCard({ onSwipe }: { onSwipe: () => void }) {
  const translateX = useSharedValue(0);

  const pan = Gesture.Pan()
    .onUpdate((event) => {
      translateX.value = event.translationX;
    })
    .onEnd((event) => {
      if (Math.abs(event.translationX) > 100) {
        runOnJS(onSwipe)();
      }
      translateX.value = withSpring(0);
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={[styles.card, animatedStyle]}>
        <Text>Swipe me</Text>
      </Animated.View>
    </GestureDetector>
  );
}
```

## Memory Management

### 컴포넌트 정리

```typescript
function Screen() {
  useEffect(() => {
    const subscription = someService.subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return <View />;
}
```

### 이미지 캐시 관리

```typescript
import { Image } from 'expo-image';

// 캐시 클리어
async function clearImageCache() {
  await Image.clearDiskCache();
  await Image.clearMemoryCache();
}

// 캐시 크기 제한
// expo-image는 자동으로 관리하지만, 필요시 수동 클리어
```

## Bundle Optimization

### Dynamic Imports

```typescript
// 조건부 로딩
const AdminPanel = lazy(() => import('@/features/admin'));

function App() {
  const { isAdmin } = useAuth();

  return (
    <View>
      {isAdmin && (
        <Suspense fallback={<Loading />}>
          <AdminPanel />
        </Suspense>
      )}
    </View>
  );
}
```

### 아이콘 최적화

```typescript
// ❌ 전체 아이콘 번들 import
import { Ionicons } from '@expo/vector-icons';

// ✅ 필요한 아이콘만 import (babel 플러그인 필요)
import HomeIcon from '@expo/vector-icons/Ionicons/home';
```

## Rendering Optimization

### useMemo for Expensive Calculations

```typescript
function ProductList({ products, filters }: Props) {
  // 필터링된 결과 메모이제이션
  const filteredProducts = useMemo(() => {
    return products
      .filter((p) => p.category === filters.category)
      .sort((a, b) => {
        if (filters.sortBy === 'price') return a.price - b.price;
        return a.name.localeCompare(b.name);
      });
  }, [products, filters.category, filters.sortBy]);

  return (
    <FlashList
      data={filteredProducts}
      renderItem={({ item }) => <ProductCard product={item} />}
      estimatedItemSize={120}
    />
  );
}
```

### useCallback for Event Handlers

```typescript
function Form() {
  const [values, setValues] = useState({ name: '', email: '' });

  // 매 렌더링마다 새 함수 생성 방지
  const handleChange = useCallback((field: string, value: string) => {
    setValues((prev) => ({ ...prev, [field]: value }));
  }, []);

  return (
    <View>
      <Input
        value={values.name}
        onChangeText={(v) => handleChange('name', v)}
      />
      <Input
        value={values.email}
        onChangeText={(v) => handleChange('email', v)}
      />
    </View>
  );
}
```

## Profiling

### React DevTools Profiler

```typescript
// 프로파일링을 위한 래퍼
import { Profiler, ProfilerOnRenderCallback } from 'react';

const onRender: ProfilerOnRenderCallback = (
  id,
  phase,
  actualDuration,
  baseDuration
) => {
  console.log(`${id} ${phase}: ${actualDuration.toFixed(2)}ms`);
};

function App() {
  return (
    <Profiler id="ProductList" onRender={onRender}>
      <ProductList products={products} />
    </Profiler>
  );
}
```

### Performance Monitoring

```typescript
// shared/lib/performance.ts
export function measurePerformance(name: string, fn: () => void) {
  const start = performance.now();
  fn();
  const end = performance.now();
  console.log(`${name}: ${(end - start).toFixed(2)}ms`);
}

// 사용
measurePerformance('filterProducts', () => {
  const filtered = products.filter((p) => p.category === 'electronics');
});
```

## Best Practices Summary

| 영역 | 권장 사항 |
|------|----------|
| Lists | FlashList + memo + keyExtractor |
| Images | expo-image + placeholder + cachePolicy |
| Animations | Reanimated (UI Thread) |
| Gestures | react-native-gesture-handler |
| Callbacks | useCallback으로 참조 안정화 |
| Calculations | useMemo로 비용 높은 연산 캐싱 |
| Components | memo로 불필요한 리렌더링 방지 |

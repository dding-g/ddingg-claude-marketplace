# Code Smell Detection Skill

> Toss Frontend Fundamentals 기반 코드 스멜 탐지 가이드

## Overview

4가지 평가 기준으로 코드 스멜을 식별하고 해결 방안을 제시합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- "코드 뭐가 문제야?" 류의 질문
- 코드 리뷰/리팩토링 요청
- 가독성, 예측 가능성, 응집도, 결합도 관련 언급

## Smell Categories

### 1. 가독성 스멜 (Readability Smells)

#### 혼재된 코드
```typescript
// ❌ Smell: UI와 로직이 혼재
const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        const filtered = data.filter(p => p.stock > 0);
        const sorted = filtered.sort((a, b) => b.price - a.price);
        setProducts(sorted);
      });
  }, []);

  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
};

// ✅ Fixed: 관심사 분리
const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
    select: (data) => data.filter(p => p.stock > 0).sort((a, b) => b.price - a.price),
  });
};

const ProductList = () => {
  const { data: products } = useProducts();
  return <ul>{products?.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
};
```

#### 노출된 구현 상세
```typescript
// ❌ Smell
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

// ✅ Fixed
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const isValidEmail = (email: string) => EMAIL_PATTERN.test(email);
```

#### 이름 없는 복잡 조건
```typescript
// ❌ Smell
if (user.age >= 19 && user.membership === 'premium' && !user.isBlocked) {
  showContent();
}

// ✅ Fixed
const canAccessPremiumContent =
  user.age >= 19 &&
  user.membership === 'premium' &&
  !user.isBlocked;

if (canAccessPremiumContent) {
  showContent();
}
```

#### 중첩된 삼항 연산자
```typescript
// ❌ Smell
const status = isLoading ? 'loading' : isError ? 'error' : data ? 'success' : 'idle';

// ✅ Fixed
const getStatus = () => {
  if (isLoading) return 'loading';
  if (isError) return 'error';
  if (data) return 'success';
  return 'idle';
};
```

#### 매직 넘버
```typescript
// ❌ Smell
if (password.length < 8) { ... }
setTimeout(callback, 3000);

// ✅ Fixed
const MIN_PASSWORD_LENGTH = 8;
const TOAST_DURATION_MS = 3000;

if (password.length < MIN_PASSWORD_LENGTH) { ... }
setTimeout(callback, TOAST_DURATION_MS);
```

### 2. 예측 가능성 스멜 (Predictability Smells)

#### 동명이상(同名異相) 함수
```typescript
// ❌ Smell: 같은 이름, 다른 동작
// utils/format.ts
export const formatDate = (date: Date) => date.toISOString();

// components/DatePicker.ts
export const formatDate = (date: Date) => date.toLocaleDateString('ko-KR');

// ✅ Fixed: 명확한 이름
export const toISOString = (date: Date) => date.toISOString();
export const toKoreanDateString = (date: Date) => date.toLocaleDateString('ko-KR');
```

#### 불일치한 반환 타입
```typescript
// ❌ Smell
const findUser = (id: string): User | null | undefined => {
  if (!id) return undefined;
  const user = users.find(u => u.id === id);
  return user ?? null;
};

// ✅ Fixed
const findUser = (id: string): User | null => {
  if (!id) return null;
  return users.find(u => u.id === id) ?? null;
};
```

#### 숨겨진 사이드 이펙트
```typescript
// ❌ Smell
const calculateTotal = (items: CartItem[]) => {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  localStorage.setItem('lastTotal', String(total)); // 숨겨진 사이드 이펙트
  return total;
};

// ✅ Fixed
const calculateTotal = (items: CartItem[]) => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

const saveTotal = (total: number) => {
  localStorage.setItem('lastTotal', String(total));
};
```

### 3. 응집도 스멜 (Cohesion Smells)

#### 종류별 파일 분류
```typescript
// ❌ Smell: 기술적 분류
// hooks/useUser.ts
// hooks/useProduct.ts
// hooks/useCart.ts
// types/user.ts
// types/product.ts
// types/cart.ts

// ✅ Fixed: 도메인별 분류 (FSD)
// entities/user/model/hooks.ts, types.ts
// entities/product/model/hooks.ts, types.ts
// entities/cart/model/hooks.ts, types.ts
```

#### 분산된 매직 넘버
```typescript
// ❌ Smell: 여러 파일에 분산
// ComponentA.tsx
const PAGE_SIZE = 20;

// ComponentB.tsx
const PAGE_SIZE = 20;

// ✅ Fixed: 한 곳에서 관리
// shared/config/pagination.ts
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
} as const;
```

#### 폼 응집도 불일치
```typescript
// ❌ Smell: 폼 관련 코드 분산
// schemas/userSchema.ts
// hooks/useUserForm.ts
// components/UserForm.tsx
// types/userForm.ts

// ✅ Fixed: 폼 관련 코드 응집
// features/create-user/
//   model/schema.ts
//   model/types.ts
//   ui/create-user-form.tsx
//   index.ts
```

### 4. 결합도 스멜 (Coupling Smells)

#### 다중 책임 Hook
```typescript
// ❌ Smell
const useUser = () => {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [followers, setFollowers] = useState([]);

  // 사용자, 게시글, 팔로워 모두 관리
  return { user, posts, followers, ... };
};

// ✅ Fixed
const useUser = (id: string) => useQuery(userQueries.detail(id));
const useUserPosts = (userId: string) => useQuery(postQueries.byUser(userId));
const useFollowers = (userId: string) => useQuery(followerQueries.byUser(userId));
```

#### 불필요한 공통화
```typescript
// ❌ Smell: 과도한 추상화
const GenericForm = ({
  fields, onSubmit, validation, layout, theme, ...rest
}: GenericFormProps) => { ... };

// ✅ Fixed: 구체적인 폼
const LoginForm = () => { ... };
const SignupForm = () => { ... };
const ProfileForm = () => { ... };
```

#### Props Drilling
```typescript
// ❌ Smell
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserMenu user={user} />
    </Sidebar>
  </Layout>
</App>

// ✅ Fixed: Context 또는 상태 관리
const UserContext = createContext<User | null>(null);
const useUser = () => useContext(UserContext);
```

## Priority Levels

| 우선순위 | 스멜 유형 |
|---------|----------|
| **높음** | 코드 혼재, 숨은 사이드 이펙트, 반환 타입 불일치 |
| **중간** | Props Drilling, 분산된 상수, 다중 책임 Hook |
| **낮음** | 파일 구조 개선, 네이밍 충돌 |

## Quick Checklist

- [ ] 함수명이 실제 동작을 반영하는가?
- [ ] 사이드 이펙트가 명시적인가?
- [ ] 관련 코드가 한 곳에 모여있는가?
- [ ] Props가 3단계 이상 전달되는가?
- [ ] 매직 넘버가 상수로 정의되어 있는가?
- [ ] 조건문이 명확한 이름을 가지는가?

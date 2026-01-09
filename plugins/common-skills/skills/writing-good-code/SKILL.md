---
name: writing-good-code
description: 읽기 쉽고 유지보수하기 좋은 코드 작성법. 네이밍, 함수 분리, Early Return 패턴 적용 시 활성화됩니다.
---

# Writing Good Code

> 읽기 쉽고, 고치기 쉬운 코드

## 핵심 원칙

### 1. 이름이 곧 문서

```typescript
// ❌
const d = new Date().getTime() - startTime;
if (d > 3000) { ... }

// ✅
const elapsedMs = new Date().getTime() - startTime;
const TIMEOUT_MS = 3000;
if (elapsedMs > TIMEOUT_MS) { ... }
```

### 2. 함수는 한 가지 일만

```typescript
// ❌ 여러 가지 일을 함
async function handleSubmit(data) {
  const validated = schema.parse(data);
  const response = await api.post('/users', validated);
  analytics.track('user_created');
  toast.success('가입 완료');
  router.push('/dashboard');
  return response;
}

// ✅ 각각의 책임을 분리
async function createUser(data) {
  return api.post('/users', schema.parse(data));
}

function handleSubmit(data) {
  createUser(data)
    .then(() => {
      analytics.track('user_created');
      toast.success('가입 완료');
      router.push('/dashboard');
    });
}
```

### 3. 조건문에 이름을 붙여라

```typescript
// ❌
if (user.age >= 19 && user.membership === 'premium' && !user.isBanned) {
  showContent();
}

// ✅
const canAccessPremiumContent =
  user.age >= 19 &&
  user.membership === 'premium' &&
  !user.isBanned;

if (canAccessPremiumContent) {
  showContent();
}
```

### 4. Early Return으로 중첩 줄이기

```typescript
// ❌
function getDiscount(user) {
  if (user) {
    if (user.membership === 'premium') {
      if (user.years > 2) {
        return 0.2;
      } else {
        return 0.1;
      }
    } else {
      return 0;
    }
  }
  return 0;
}

// ✅
function getDiscount(user) {
  if (!user) return 0;
  if (user.membership !== 'premium') return 0;
  if (user.years > 2) return 0.2;
  return 0.1;
}
```

### 5. 관련 코드는 가까이

```typescript
// ❌ 타입, 상수, 유틸이 각각 다른 폴더에
import { User } from '@/types/user';
import { USER_STATUS } from '@/constants/user';
import { formatUserName } from '@/utils/user';

// ✅ 함께 사용되는 코드는 함께
// features/user/index.ts
export interface User { ... }
export const USER_STATUS = { ... };
export function formatUserName(user: User) { ... }
```

## 컴포넌트 작성

### Props는 필요한 것만

```typescript
// ❌ 전체 객체 전달
function UserAvatar({ user }: { user: User }) {
  return <img src={user.avatar} alt={user.name} />;
}

// ✅ 필요한 것만
function UserAvatar({ src, alt }: { src: string; alt: string }) {
  return <img src={src} alt={alt} />;
}
```

### 조건부 렌더링은 심플하게

```typescript
// ❌ 삼항 중첩
{isLoading ? <Spinner /> : error ? <Error /> : data ? <Content /> : null}

// ✅ Early Return 패턴
function Component() {
  if (isLoading) return <Spinner />;
  if (error) return <Error />;
  if (!data) return null;
  return <Content data={data} />;
}
```

### 커스텀 훅으로 로직 추출

```typescript
// ❌ 컴포넌트에 로직이 섞임
function SearchResults() {
  const [query, setQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(query), 300);
    return () => clearTimeout(timer);
  }, [query]);

  const { data } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => search(debouncedQuery),
    enabled: debouncedQuery.length > 0,
  });

  return (/* UI */);
}

// ✅ 로직은 훅으로, 컴포넌트는 UI만
function useSearch() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  const { data } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => search(debouncedQuery),
    enabled: debouncedQuery.length > 0,
  });

  return { query, setQuery, results: data };
}

function SearchResults() {
  const { query, setQuery, results } = useSearch();
  return (/* UI */);
}
```

## 흔한 실수

### 불필요한 상태

```typescript
// ❌ 파생 가능한 값을 상태로
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0);

useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0));
}, [items]);

// ✅ 계산으로 파생
const [items, setItems] = useState([]);
const total = items.reduce((sum, item) => sum + item.price, 0);
```

### 숨겨진 사이드 이펙트

```typescript
// ❌ 이름과 다른 동작
function formatPrice(price: number) {
  analytics.track('price_viewed'); // ??
  return `$${price.toFixed(2)}`;
}

// ✅ 명확한 분리
function formatPrice(price: number) {
  return `$${price.toFixed(2)}`;
}

function trackPriceView() {
  analytics.track('price_viewed');
}
```

### 과도한 추상화

```typescript
// ❌ 2번 쓰일지도 모르니까 미리 추상화
function GenericModal<T>({
  data,
  renderHeader,
  renderBody,
  renderFooter,
  onClose,
  ...rest
}: GenericModalProps<T>) { ... }

// ✅ 구체적으로 시작, 필요할 때 추상화
function ConfirmDeleteModal({ onConfirm, onCancel }) { ... }
function EditUserModal({ user, onSave, onCancel }) { ... }
```

## 기억할 것

- 코드는 쓰는 것보다 읽히는 횟수가 훨씬 많다
- 3개월 후의 나는 이 코드를 이해할 수 있을까?
- "동작하는 코드"보다 "이해되는 코드"
- 미래의 요구사항을 예측하지 마라. 지금 필요한 것만 작성하라

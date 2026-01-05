# TypeScript Patterns

> 실용적 타입 작성법

## 타입 추론 활용하기

```typescript
// ❌ 불필요한 타입 명시
const name: string = 'John';
const items: string[] = ['a', 'b', 'c'];
const user: { name: string; age: number } = { name: 'John', age: 30 };

// ✅ 추론에 맡기기
const name = 'John';
const items = ['a', 'b', 'c'];
const user = { name: 'John', age: 30 };
```

**타입을 명시할 때**: 함수 파라미터, 함수 반환값(복잡한 경우), export 타입

## 유틸리티 타입

### 자주 쓰는 것들

```typescript
// Partial: 모두 optional
type UpdateUser = Partial<User>;

// Pick: 일부만 선택
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit: 일부 제외
type CreateUser = Omit<User, 'id' | 'createdAt'>;

// Required: 모두 필수
type RequiredConfig = Required<Config>;

// Record: 키-값 맵
type UserMap = Record<string, User>;
```

### 조합해서 사용

```typescript
// id는 필수, 나머지는 optional
type UpdateUser = Partial<User> & { id: string };

// 특정 필드만 optional
type CreateUser = Omit<User, 'id'> & { id?: string };
```

## 타입 좁히기 (Narrowing)

### typeof, in, instanceof

```typescript
function process(input: string | number) {
  if (typeof input === 'string') {
    return input.toUpperCase(); // string으로 좁혀짐
  }
  return input.toFixed(2); // number로 좁혀짐
}

function handleResponse(res: SuccessResponse | ErrorResponse) {
  if ('error' in res) {
    console.error(res.error); // ErrorResponse
    return;
  }
  return res.data; // SuccessResponse
}
```

### Discriminated Union (권장)

```typescript
type Result =
  | { status: 'success'; data: User }
  | { status: 'error'; error: Error }
  | { status: 'loading' };

function handleResult(result: Result) {
  switch (result.status) {
    case 'success':
      return result.data; // User 타입
    case 'error':
      throw result.error; // Error 타입
    case 'loading':
      return null;
  }
}
```

### 타입 가드

```typescript
// 커스텀 타입 가드
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

// 사용
const data: unknown = await fetchData();
if (isUser(data)) {
  console.log(data.name); // User 타입으로 안전하게 사용
}
```

## 제네릭

### 기본 패턴

```typescript
// API 응답 래퍼
interface ApiResponse<T> {
  data: T;
  status: number;
}

// 사용
const response: ApiResponse<User> = await api.get('/user');
```

### 제네릭 제약

```typescript
// T는 반드시 id를 가져야 함
function findById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}
```

### 컴포넌트 제네릭

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// 사용 - 타입 추론됨
<List
  items={users}
  renderItem={(user) => <span>{user.name}</span>}
  keyExtractor={(user) => user.id}
/>
```

## as const

```typescript
// 리터럴 타입으로 고정
const ROUTES = {
  HOME: '/',
  ABOUT: '/about',
  USER: '/user',
} as const;

type Route = typeof ROUTES[keyof typeof ROUTES]; // '/' | '/about' | '/user'

// 배열도 마찬가지
const STATUSES = ['pending', 'active', 'done'] as const;
type Status = typeof STATUSES[number]; // 'pending' | 'active' | 'done'
```

## 피해야 할 패턴

```typescript
// ❌ any 사용
function process(data: any) { ... }

// ✅ unknown + 타입 가드
function process(data: unknown) {
  if (isValidData(data)) { ... }
}

// ❌ 타입 단언 남용
const user = data as User;

// ✅ 타입 가드로 안전하게
if (isUser(data)) {
  const user = data;
}

// ❌ non-null assertion 남발
const name = user!.name!;

// ✅ optional chaining + nullish coalescing
const name = user?.name ?? 'Unknown';

// ❌ enum (트리쉐이킹 안됨)
enum Status { Active, Inactive }

// ✅ as const + 유니온
const Status = { Active: 'active', Inactive: 'inactive' } as const;
type Status = typeof Status[keyof typeof Status];
```

## 실용적 팁

```typescript
// 컴포넌트 Props 타입
type ButtonProps = React.ComponentProps<'button'> & {
  variant?: 'primary' | 'secondary';
};

// 이벤트 핸들러 타입
const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
  setValue(e.target.value);
};

// Promise 반환 타입
async function fetchUser(id: string): Promise<User> {
  const response = await api.get(`/users/${id}`);
  return response.data;
}
```

**핵심**: 타입은 문서이자 안전장치. 복잡하게 만들지 말고, 명확하게 의도를 표현하세요.

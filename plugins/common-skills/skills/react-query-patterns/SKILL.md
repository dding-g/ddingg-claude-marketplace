---
name: react-query-patterns
description: React Query 서버 상태 관리 패턴. Query Factory, queryOptions, mutationOptions 패턴 적용 시 활성화됩니다.
---

# React Query Patterns

> 서버 상태 관리 - Query Factory와 Options 패턴

## 폴더 구조

```
entities/user/api/
├── keys.ts          # Query Key Factory
├── get-user.ts      # 개별 API 함수
├── get-users.ts
├── create-user.ts
├── update-user.ts
├── query.ts         # queryOptions 정의
└── mutation.ts      # mutationOptions 정의
```

## 1. Query Key Factory

모든 Query Key는 Factory 패턴으로 관리합니다.

```typescript
// entities/user/api/keys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};
```

**캐시 무효화 예시:**

```typescript
// 특정 유저만 무효화
queryClient.invalidateQueries({ queryKey: userKeys.detail(userId) });

// 모든 detail 쿼리 무효화
queryClient.invalidateQueries({ queryKey: userKeys.details() });

// 모든 list 쿼리 무효화
queryClient.invalidateQueries({ queryKey: userKeys.lists() });

// 전체 users 캐시 무효화
queryClient.invalidateQueries({ queryKey: userKeys.all });
```

## 2. API 함수 분리

API 함수는 개별 파일로 분리합니다.

```typescript
// entities/user/api/get-user.ts
import { api } from '@/shared/api';
import type { User } from '../model/types';

export async function getUser(id: string): Promise<User> {
  const response = await api.get<User>(`/users/${id}`);
  return response.data;
}
```

```typescript
// entities/user/api/get-users.ts
import { api } from '@/shared/api';
import type { User, UserFilters } from '../model/types';

export async function getUsers(filters?: UserFilters): Promise<User[]> {
  const response = await api.get<User[]>('/users', { params: filters });
  return response.data;
}
```

```typescript
// entities/user/api/create-user.ts
import { api } from '@/shared/api';
import type { User, CreateUserDto } from '../model/types';

export async function createUser(data: CreateUserDto): Promise<User> {
  const response = await api.post<User>('/users', data);
  return response.data;
}
```

```typescript
// entities/user/api/update-user.ts
import { api } from '@/shared/api';
import type { User, UpdateUserDto } from '../model/types';

export async function updateUser(id: string, data: UpdateUserDto): Promise<User> {
  const response = await api.patch<User>(`/users/${id}`, data);
  return response.data;
}
```

## 3. queryOptions 패턴

모든 Query는 queryOptions로 정의합니다.

```typescript
// entities/user/api/query.ts
import { queryOptions } from '@tanstack/react-query';
import { userKeys } from './keys';
import { getUser } from './get-user';
import { getUsers } from './get-users';

export const userQueries = {
  all: () => queryOptions({
    queryKey: userKeys.all,
  }),

  list: (filters?: UserFilters) => queryOptions({
    queryKey: userKeys.list(filters ?? {}),
    queryFn: () => getUsers(filters),
  }),

  detail: (id: string) => queryOptions({
    queryKey: userKeys.detail(id),
    queryFn: () => getUser(id),
    staleTime: 5 * 60 * 1000, // 5분
  }),
};
```

**사용 예시:**

```typescript
// 컴포넌트에서 사용
const { data } = useQuery(userQueries.detail(userId));
const { data } = useSuspenseQuery(userQueries.detail(userId));

// prefetch
await queryClient.prefetchQuery(userQueries.detail(userId));

// ensureQueryData
const user = await queryClient.ensureQueryData(userQueries.detail(userId));
```

## 4. mutationOptions 패턴

모든 Mutation은 mutationOptions로 정의합니다.

```typescript
// entities/user/api/mutation.ts
import { mutationOptions } from '@tanstack/react-query';
import { userKeys } from './keys';
import { createUser } from './create-user';
import { updateUser } from './update-user';
import { deleteUser } from './delete-user';

export const userMutations = {
  create: () => mutationOptions({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  }),

  update: () => mutationOptions({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserDto }) =>
      updateUser(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: userKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  }),

  delete: () => mutationOptions({
    mutationFn: deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.all });
    },
  }),
};
```

**사용 예시:**

```typescript
// 컴포넌트에서 사용
const createUserMutation = useMutation(userMutations.create());
const updateUserMutation = useMutation(userMutations.update());

// 실행
createUserMutation.mutate({ name: '홍길동', email: 'hong@example.com' });
updateUserMutation.mutate({ id: userId, data: { name: '김철수' } });
```

## 5. Optimistic Update

UX가 중요한 인터랙션에서 사용합니다.

```typescript
// entities/user/api/mutation.ts
export const userMutations = {
  update: () => mutationOptions({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserDto }) =>
      updateUser(id, data),
    onMutate: async ({ id, data }) => {
      // 진행 중인 쿼리 취소
      await queryClient.cancelQueries({ queryKey: userKeys.detail(id) });

      // 이전 데이터 백업
      const previousUser = queryClient.getQueryData(userKeys.detail(id));

      // 낙관적 업데이트
      queryClient.setQueryData(userKeys.detail(id), (old: User) => ({
        ...old,
        ...data,
      }));

      return { previousUser };
    },
    onError: (err, { id }, context) => {
      // 에러 시 롤백
      if (context?.previousUser) {
        queryClient.setQueryData(userKeys.detail(id), context.previousUser);
      }
    },
    onSettled: (_, __, { id }) => {
      // 서버 데이터로 동기화
      queryClient.invalidateQueries({ queryKey: userKeys.detail(id) });
    },
  }),
};
```

## 6. Suspense와 함께

```typescript
// Suspense + ErrorBoundary 조합
<ErrorBoundary fallback={<Error />}>
  <Suspense fallback={<Loading />}>
    <UserProfile userId={userId} />
  </Suspense>
</ErrorBoundary>

function UserProfile({ userId }: { userId: string }) {
  // useSuspenseQuery: 로딩/에러를 상위로 위임
  const { data } = useSuspenseQuery(userQueries.detail(userId));
  return <div>{data.name}</div>;  // data는 항상 존재
}
```

## 실용적 팁

### staleTime 설정

```typescript
export const userQueries = {
  // 자주 변하지 않는 데이터
  profile: (id: string) => queryOptions({
    queryKey: userKeys.detail(id),
    queryFn: () => getUser(id),
    staleTime: Infinity,  // 수동 무효화 전까지 fresh
  }),

  // 실시간성이 중요한 데이터
  notifications: () => queryOptions({
    queryKey: ['notifications'],
    queryFn: fetchNotifications,
    staleTime: 0,
    refetchInterval: 30000,  // 30초마다 폴링
  }),
};
```

### 전역 설정

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1분
      retry: 1,
      throwOnError: true,  // ErrorBoundary로 전파
    },
  },
});
```

## 하지 말아야 할 것

```typescript
// ❌ queryKey 직접 사용
useQuery({ queryKey: ['user', userId] });

// ✅ Query Key Factory 사용
useQuery(userQueries.detail(userId));


// ❌ queryFn에 직접 API 호출
useQuery({
  queryKey: userKeys.detail(id),
  queryFn: () => api.get(`/users/${id}`),
});

// ✅ 분리된 API 함수 사용
useQuery(userQueries.detail(id));


// ❌ inline으로 mutation 정의
useMutation({
  mutationFn: (data) => api.post('/users', data),
});

// ✅ mutationOptions 사용
useMutation(userMutations.create());


// ❌ queryFn 안에서 조건부 로직
useQuery({
  queryFn: () => (isAdmin ? fetchAdminData() : fetchUserData()),
});

// ✅ 별도의 queryOptions로 분리
useQuery(isAdmin ? adminQueries.data() : userQueries.data());
```

## 전체 예시

```
entities/user/
├── api/
│   ├── index.ts         # re-export
│   ├── keys.ts          # Query Key Factory
│   ├── get-user.ts
│   ├── get-users.ts
│   ├── create-user.ts
│   ├── update-user.ts
│   ├── delete-user.ts
│   ├── query.ts         # queryOptions
│   └── mutation.ts      # mutationOptions
├── model/
│   └── types.ts         # 타입 정의
└── index.ts             # Public API
```

```typescript
// entities/user/api/index.ts
export { userKeys } from './keys';
export { userQueries } from './query';
export { userMutations } from './mutation';
```

```typescript
// 컴포넌트에서 사용
import { userQueries, userMutations } from '@/entities/user/api';

function UserPage({ userId }: { userId: string }) {
  const { data: user } = useSuspenseQuery(userQueries.detail(userId));
  const updateMutation = useMutation(userMutations.update());

  const handleUpdate = (data: UpdateUserDto) => {
    updateMutation.mutate({ id: userId, data });
  };

  return <UserForm user={user} onSubmit={handleUpdate} />;
}
```

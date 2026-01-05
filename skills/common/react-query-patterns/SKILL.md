# React Query Patterns Skill

> TanStack Query 패턴 및 베스트 프랙티스 가이드

## Overview

React Query(TanStack Query)를 사용한 서버 상태 관리의 표준 패턴을 제공합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- React Query, TanStack Query 언급
- 데이터 페칭 관련 질문
- useQuery, useMutation 사용
- 캐시 관리, 낙관적 업데이트 관련

## Core Patterns

### 1. Query Key Factory

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

### 2. Query Options Factory

```typescript
// entities/user/api/queries.ts
import { queryOptions } from '@tanstack/react-query';

export const userQueries = {
  list: (filters: UserFilters) => queryOptions({
    queryKey: userKeys.list(filters),
    queryFn: () => api.get<User[]>('/users', { params: filters }),
    staleTime: 1000 * 60 * 5, // 5분
  }),

  detail: (id: string) => queryOptions({
    queryKey: userKeys.detail(id),
    queryFn: () => api.get<User>(`/users/${id}`),
    enabled: !!id,
  }),
};
```

### 3. Suspense Query Hook

```typescript
// entities/user/api/hooks.ts
import { useSuspenseQuery } from '@tanstack/react-query';

export const useUser = (id: string) => {
  return useSuspenseQuery(userQueries.detail(id));
};

export const useUsers = (filters: UserFilters) => {
  return useSuspenseQuery(userQueries.list(filters));
};
```

### 4. Mutation with Optimistic Update

```typescript
// features/user/api/mutations.ts
export const useUpdateUserMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateUserDto) =>
      api.patch<User>(`/users/${data.id}`, data),

    onMutate: async (newData) => {
      await queryClient.cancelQueries({
        queryKey: userKeys.detail(newData.id)
      });

      const previous = queryClient.getQueryData(
        userKeys.detail(newData.id)
      );

      queryClient.setQueryData(
        userKeys.detail(newData.id),
        (old: User) => ({ ...old, ...newData })
      );

      return { previous };
    },

    onError: (err, newData, context) => {
      queryClient.setQueryData(
        userKeys.detail(newData.id),
        context?.previous
      );
    },

    onSettled: (data, err, variables) => {
      queryClient.invalidateQueries({
        queryKey: userKeys.detail(variables.id)
      });
    },
  });
};
```

## FSD Integration

```
entities/user/
├── api/
│   ├── keys.ts       # Query Key Factory
│   ├── queries.ts    # queryOptions Factory
│   └── hooks.ts      # useSuspenseQuery Hooks
├── model/
│   └── types.ts      # User 타입 정의
└── index.ts

features/update-user/
├── api/
│   └── mutations.ts  # useMutation Hooks
├── ui/
│   └── update-form.tsx
└── index.ts
```

## QueryClient Setup

```typescript
// shared/api/query-client.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60, // 1분
      gcTime: 1000 * 60 * 5, // 5분
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});
```

## Advanced Patterns

### Dependent Queries

```typescript
const useUserPosts = (userId: string) => {
  const { data: user } = useUser(userId);

  return useQuery({
    ...postQueries.listByUser(user.id),
    enabled: !!user,
  });
};
```

### Infinite Query

```typescript
export const useInfiniteUsers = (filters: UserFilters) => {
  return useInfiniteQuery({
    queryKey: userKeys.list(filters),
    queryFn: ({ pageParam = 0 }) =>
      api.get<PaginatedUsers>('/users', {
        params: { ...filters, page: pageParam },
      }),
    getNextPageParam: (lastPage) => lastPage.nextPage,
    initialPageParam: 0,
  });
};
```

### Prefetching

```typescript
// 라우트 진입 전 prefetch
const prefetchUser = async (id: string) => {
  await queryClient.prefetchQuery(userQueries.detail(id));
};

// 컴포넌트에서 hover prefetch
const UserCard = ({ userId }: { userId: string }) => {
  const prefetch = () => {
    queryClient.prefetchQuery(userQueries.detail(userId));
  };

  return (
    <Link
      to={`/users/${userId}`}
      onMouseEnter={prefetch}
    >
      ...
    </Link>
  );
};
```

## Best Practices

1. **Query vs Mutation 분리**: GET은 queries, POST/PUT/DELETE는 mutations
2. **계층적 캐시 무효화**: queryKey 계층 구조 활용
3. **Suspense 패턴**: useSuspenseQuery로 로딩 상태 단순화
4. **낙관적 업데이트**: UX 향상을 위한 즉각적 피드백
5. **에러 바운더리**: Suspense + ErrorBoundary 조합

## Troubleshooting

### 캐시가 업데이트되지 않음

```typescript
// ❌ 잘못된 방법 - 새 참조 생성
queryClient.setQueryData(key, { ...old, ...new });

// ✅ 올바른 방법 - 함수로 업데이트
queryClient.setQueryData(key, (old) => ({ ...old, ...new }));
```

### 무한 리렌더링

```typescript
// ❌ 매번 새 객체 생성
useQuery({ queryKey: ['users', { page }] });

// ✅ useMemo로 안정화
const filters = useMemo(() => ({ page }), [page]);
useQuery({ queryKey: ['users', filters] });
```

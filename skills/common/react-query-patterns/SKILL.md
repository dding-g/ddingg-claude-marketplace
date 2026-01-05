# React Query Patterns

> 서버 상태 관리 - 심플하게 시작하기

## 기본 패턴

### Query

```typescript
// 가장 기본적인 형태로 시작
const { data, isLoading, error } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => api.get(`/users/${userId}`),
});
```

### Mutation

```typescript
const { mutate, isPending } = useMutation({
  mutationFn: (data) => api.post('/users', data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
  },
});
```

이것만으로 대부분의 케이스를 커버합니다.

## 패턴 확장 (필요할 때만)

### queryOptions (TanStack Query v5+)

여러 곳에서 같은 쿼리를 재사용할 때:

```typescript
// entities/user/queries.ts
export const userQueries = {
  detail: (id: string) => queryOptions({
    queryKey: ['user', id],
    queryFn: () => api.get(`/users/${id}`),
  }),
};

// 사용
const { data } = useQuery(userQueries.detail(userId));
const { data } = useSuspenseQuery(userQueries.detail(userId));
await queryClient.prefetchQuery(userQueries.detail(userId));
```

### Query Key Factory

캐시 무효화가 복잡해질 때만 도입:

```typescript
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  detail: (id: string) => [...userKeys.all, id] as const,
};

// 전체 users 캐시 무효화
queryClient.invalidateQueries({ queryKey: userKeys.all });
```

### Optimistic Update

UX가 중요한 인터랙션에서만:

```typescript
useMutation({
  mutationFn: updateUser,
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['user', newData.id] });
    const previous = queryClient.getQueryData(['user', newData.id]);
    queryClient.setQueryData(['user', newData.id], newData);
    return { previous };
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(['user', newData.id], context?.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['user'] });
  },
});
```

복잡합니다. 정말 필요할 때만 사용하세요.

## 실용적 팁

### staleTime 설정

```typescript
// 자주 변하지 않는 데이터
useQuery({
  queryKey: ['config'],
  queryFn: fetchConfig,
  staleTime: Infinity,  // 수동 무효화 전까지 fresh
});

// 실시간성이 중요한 데이터
useQuery({
  queryKey: ['notifications'],
  queryFn: fetchNotifications,
  staleTime: 0,  // 항상 stale (기본값)
  refetchInterval: 30000,  // 30초마다 폴링
});
```

### 에러 처리

```typescript
// 전역 에러 처리
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      throwOnError: true,  // ErrorBoundary로 전파
    },
  },
});

// 개별 쿼리에서 에러 처리
const { data, error } = useQuery({
  queryKey: ['user', id],
  queryFn: fetchUser,
  throwOnError: false,  // 컴포넌트에서 직접 처리
});

if (error) return <ErrorMessage error={error} />;
```

### Suspense와 함께

```typescript
// Suspense + ErrorBoundary 조합
<ErrorBoundary fallback={<Error />}>
  <Suspense fallback={<Loading />}>
    <UserProfile />
  </Suspense>
</ErrorBoundary>

function UserProfile() {
  // useSuspenseQuery: 로딩/에러를 상위로 위임
  const { data } = useSuspenseQuery(userQueries.detail(userId));
  return <div>{data.name}</div>;  // data는 항상 존재
}
```

## 하지 말아야 할 것

```typescript
// ❌ queryKey에 함수나 불안정한 참조
useQuery({ queryKey: ['users', { filter: () => {} }] });

// ❌ queryFn 안에서 조건부 로직
useQuery({
  queryFn: () => (isAdmin ? fetchAdminData() : fetchUserData()),
});

// ❌ 불필요한 상태 동기화
const { data } = useQuery({ queryKey: ['user'] });
const [user, setUser] = useState(data);  // 왜?
```

심플하게 시작하고, 필요할 때 확장하세요.

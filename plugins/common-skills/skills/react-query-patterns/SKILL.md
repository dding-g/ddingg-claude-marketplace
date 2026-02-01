---
name: react-query-patterns
description: React Query server state management patterns. Activated when applying Query Factory, queryOptions, or mutationOptions patterns.
---

# React Query Patterns

> Server state management - Query Factory & Options patterns

## File Structure

```
entities/user/api/
├── keys.ts          # Query Key Factory
├── get-user.ts      # Individual API functions
├── get-users.ts
├── create-user.ts
├── update-user.ts
├── query.ts         # queryOptions definitions
└── mutation.ts      # mutationOptions definitions
```

## 1. Query Key Factory

All Query Keys managed via Factory pattern.

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

Cache invalidation:

```typescript
queryClient.invalidateQueries({ queryKey: userKeys.detail(userId) }); // specific user
queryClient.invalidateQueries({ queryKey: userKeys.details() });      // all details
queryClient.invalidateQueries({ queryKey: userKeys.lists() });        // all lists
queryClient.invalidateQueries({ queryKey: userKeys.all });            // everything
```

## 2. API Functions

Separate API functions into individual files.

```typescript
// entities/user/api/get-user.ts
import { api } from '@/shared/api';
import type { User } from '../model/types';

export async function getUser(id: string): Promise<User> {
  const response = await api.get<User>(`/users/${id}`);
  return response.data;
}
```

## 3. queryOptions Pattern

All Queries defined via queryOptions.

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
    staleTime: 5 * 60 * 1000,
  }),
};
```

Usage:

```typescript
const { data } = useQuery(userQueries.detail(userId));
const { data } = useSuspenseQuery(userQueries.detail(userId));
await queryClient.prefetchQuery(userQueries.detail(userId));
const user = await queryClient.ensureQueryData(userQueries.detail(userId));
```

## 4. mutationOptions Pattern

All Mutations defined via mutationOptions.

```typescript
// entities/user/api/mutation.ts
import { mutationOptions } from '@tanstack/react-query';
import { userKeys } from './keys';
import { createUser } from './create-user';
import { updateUser } from './update-user';

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
};
```

Usage:

```typescript
const createUserMutation = useMutation(userMutations.create());
createUserMutation.mutate({ name: 'John', email: 'john@example.com' });
```

## 5. Optimistic Update

```typescript
export const userMutations = {
  update: () => mutationOptions({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserDto }) =>
      updateUser(id, data),
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: userKeys.detail(id) });
      const previousUser = queryClient.getQueryData(userKeys.detail(id));
      queryClient.setQueryData(userKeys.detail(id), (old: User) => ({
        ...old,
        ...data,
      }));
      return { previousUser };
    },
    onError: (err, { id }, context) => {
      if (context?.previousUser) {
        queryClient.setQueryData(userKeys.detail(id), context.previousUser);
      }
    },
    onSettled: (_, __, { id }) => {
      queryClient.invalidateQueries({ queryKey: userKeys.detail(id) });
    },
  }),
};
```

## 6. Suspense Integration

```typescript
<ErrorBoundary fallback={<Error />}>
  <Suspense fallback={<Loading />}>
    <UserProfile userId={userId} />
  </Suspense>
</ErrorBoundary>

function UserProfile({ userId }: { userId: string }) {
  const { data } = useSuspenseQuery(userQueries.detail(userId));
  return <div>{data.name}</div>;  // data is always defined
}
```

## staleTime Guide

|Data Type|staleTime|Notes|
|---|---|---|
|Rarely changing|`Infinity`|Manual invalidation only|
|Standard|`5 * 60 * 1000`|5 min|
|Real-time|`0` + `refetchInterval`|Polling|

Global defaults:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      retry: 1,
      throwOnError: true,
    },
  },
});
```

## Full Example Structure

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
│   └── types.ts
└── index.ts             # Public API
```

## DO NOT

```typescript
// AVOID: inline queryKey
useQuery({ queryKey: ['user', userId] });
// USE: Query Key Factory
useQuery(userQueries.detail(userId));

// AVOID: inline API call in queryFn
useQuery({
  queryKey: userKeys.detail(id),
  queryFn: () => api.get(`/users/${id}`),
});
// USE: separated API function via queryOptions
useQuery(userQueries.detail(id));

// AVOID: inline mutation definition
useMutation({ mutationFn: (data) => api.post('/users', data) });
// USE: mutationOptions
useMutation(userMutations.create());

// AVOID: conditional logic in queryFn
useQuery({ queryFn: () => (isAdmin ? fetchAdminData() : fetchUserData()) });
// USE: separate queryOptions
useQuery(isAdmin ? adminQueries.data() : userQueries.data());
```

---
name: fsd-architecture
description: Feature-Sliced Design architecture patterns. Activated when working with FSD layers, slices, dependency rules, or structuring frontend code.
---

# FSD Architecture

> Feature-Sliced Design - frontend standard architecture

## Layer Structure

```
src/
├── app/        # App init, providers, router, global styles
├── pages/      # Route entry points (composition only, no logic)
├── widgets/    # Independent UI block compositions
├── features/   # User actions (login, like, comment)
├── entities/   # Business entities (User, Product, Order)
└── shared/     # Common utils, UI Kit, API client
```

## Dependency Rules (Mandatory)

```
app     → pages, widgets, features, entities, shared
pages   → widgets, features, entities, shared
widgets → features, entities, shared
features → entities, shared
entities → shared
shared   → (external libraries only)
```

**Import only from lower layers. No exceptions.**

```typescript
// features/auth/ui/login-form.tsx
import { User } from '@/entities/user';       // OK: lower layer
import { Button } from '@/shared/ui';          // OK: lower layer

// entities/user/model/hooks.ts
import { useAuth } from '@/features/auth';     // FORBIDDEN: upper layer

// features/auth/ui/login-form.tsx
import { useProfile } from '@/features/profile'; // FORBIDDEN: same layer cross-slice
```

## Slice Structure

```
features/auth/
├── ui/              # Components
│   ├── login-form.tsx
│   └── logout-button.tsx
├── model/           # State, types
│   ├── types.ts
│   └── store.ts
├── api/             # API calls, React Query
│   ├── queries.ts
│   └── mutations.ts
├── lib/             # Utilities
│   └── validate-token.ts
└── index.ts         # Public API (required)
```

## Public API (Required)

Every slice must export through `index.ts`.

```typescript
// features/auth/index.ts
export { LoginForm } from './ui/login-form';
export { LogoutButton } from './ui/logout-button';
export { useLoginMutation } from './api/mutations';
export type { LoginCredentials } from './model/types';
```

```typescript
// OK
import { LoginForm, useLoginMutation } from '@/features/auth';

// FORBIDDEN: direct internal access
import { LoginForm } from '@/features/auth/ui/login-form';
```

## Layer Roles

|Layer|Role|Key Rules|
|---|---|---|
|app/|Provider setup, global styles, router config|No business logic|
|pages/|Route entry points|Compose widgets/features only, no business logic|
|widgets/|Independent UI blocks|Combine features + entities, page-ready units|
|features/|User action units|Business logic, mutations live here|
|entities/|Business entities|Type definitions, queries (read-only)|
|shared/|Project-independent code|UI Kit, utilities, API client|

```typescript
// pages/dashboard/index.tsx
export function DashboardPage() {
  return (
    <PageLayout>
      <DashboardHeader />      {/* widgets */}
      <DashboardStats />       {/* widgets */}
      <RecentActivity />       {/* widgets */}
    </PageLayout>
  );
}
```

```typescript
// widgets/user-profile/index.tsx
export function UserProfile({ userId }: Props) {
  const { data: user } = useUser(userId);
  const { mutate: follow } = useFollowMutation();

  return (
    <Card>
      <UserAvatar user={user} />
      <UserInfo user={user} />
      <FollowButton onFollow={() => follow(userId)} />
    </Card>
  );
}
```

```typescript
// features/like-post/api/mutations.ts
export const useLikePostMutation = () => {
  return useMutation({
    mutationFn: (postId: string) => api.post(`/posts/${postId}/like`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: postKeys.all });
    },
  });
};
```

```typescript
// entities/user/api/queries.ts
export const userQueries = {
  detail: (id: string) => queryOptions({
    queryKey: ['user', id],
    queryFn: () => api.get<User>(`/users/${id}`),
  }),
};
```

## Naming Conventions

|Target|Rule|Example|
|---|---|---|
|Layer|lowercase|`features`, `entities`|
|Slice|kebab-case|`user-profile`, `create-post`|
|Component file|kebab-case|`login-form.tsx`|
|Component|PascalCase|`LoginForm`|
|Hook|camelCase|`useUser`, `useLoginMutation`|
|Type|PascalCase|`User`, `LoginCredentials`|

## tsconfig Paths

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Circular Reference Resolution

When circular references occur, move shared types to `shared`:

```typescript
// shared/types/index.ts
export interface BaseUser { id: string; name: string; }
export interface BasePost { id: string; authorId: string; }
```

## DO NOT

- Import from upper layers
- Import from same-layer sibling slices
- Bypass `index.ts` public API
- Put business logic in `pages/` layer
- Put mutations in `entities/` layer (read-only)

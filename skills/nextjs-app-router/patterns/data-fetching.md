# Next.js Data Fetching Patterns

## Fetch Options

### Static Data (SSG)

```typescript
// 빌드 시 한 번만 페칭
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache', // default
});
```

### Dynamic Data (SSR)

```typescript
// 매 요청마다 페칭
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});
```

### Incremental Static Regeneration (ISR)

```typescript
// 지정된 시간마다 재검증
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }, // 1시간
});
```

### Tag-based Revalidation

```typescript
// 태그 기반 캐시 무효화
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] },
});

// Server Action에서 캐시 무효화
import { revalidateTag } from 'next/cache';

export async function createPost() {
  // ... 포스트 생성
  revalidateTag('posts');
}
```

## React Cache

```typescript
import { cache } from 'react';

// 동일한 인자로 호출 시 중복 요청 방지
export const getUser = cache(async (id: string) => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
});

// 여러 컴포넌트에서 호출해도 한 번만 실행
async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId);
  // ...
}

async function UserAvatar({ userId }: { userId: string }) {
  const user = await getUser(userId); // 캐시된 결과 재사용
  // ...
}
```

## Parallel Fetching

```typescript
async function Dashboard() {
  // ✅ 병렬 실행
  const [user, posts, stats] = await Promise.all([
    getUser(),
    getPosts(),
    getStats(),
  ]);

  return <DashboardContent user={user} posts={posts} stats={stats} />;
}
```

## Sequential Fetching (Waterfall)

```typescript
async function UserPosts({ userId }: { userId: string }) {
  // 순차 실행이 필요한 경우
  const user = await getUser(userId);
  const posts = await getPostsByAuthor(user.id);

  return <PostList posts={posts} />;
}
```

## Preloading

```typescript
// lib/preload.ts
import { getUser } from './queries';

export const preloadUser = (id: string) => {
  void getUser(id);
};

// page.tsx
import { preloadUser } from '@/lib/preload';

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  preloadUser(id); // 미리 시작

  // 다른 작업 수행
  const config = await getConfig();

  // 이미 캐시되어 있음
  const user = await getUser(id);

  return <UserProfile user={user} config={config} />;
}
```

## Client-Side Fetching (React Query)

```typescript
'use client';

import { useQuery } from '@tanstack/react-query';

export function RealtimeNotifications() {
  const { data, isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: fetchNotifications,
    refetchInterval: 5000, // 5초마다 폴링
  });

  if (isLoading) return <Skeleton />;

  return <NotificationList notifications={data} />;
}
```

## Hybrid Approach

```typescript
// Server Component에서 초기 데이터 페칭
async function PostsPage() {
  const initialPosts = await getPosts();

  return (
    <PostsProvider initialData={initialPosts}>
      <PostsList />
    </PostsProvider>
  );
}

// Client Component에서 React Query로 관리
'use client';

function PostsList() {
  const { data: posts } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
    // Server에서 받은 초기 데이터 사용
    initialData: usePostsContext(),
  });

  return <ul>{posts.map(post => <PostItem key={post.id} post={post} />)}</ul>;
}
```

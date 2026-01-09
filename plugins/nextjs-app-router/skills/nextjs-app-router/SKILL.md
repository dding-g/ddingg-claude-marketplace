# Next.js App Router Skill

> Next.js 15+ App Router 기반 모던 프론트엔드 개발 가이드

## Overview

Next.js App Router의 최신 패턴과 베스트 프랙티스를 제공합니다. Server Components, Server Actions, 그리고 모던 렌더링 전략을 다룹니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- Next.js, App Router 언급
- Server Components, Server Actions 관련
- 페이지 라우팅, 레이아웃 구성
- 렌더링 전략 (SSR, SSG, ISR) 관련

## Project Structure (FSD + App Router)

```
src/
├── app/                      # Next.js App Router
│   ├── (auth)/               # Route Group
│   │   ├── login/
│   │   └── signup/
│   ├── (main)/
│   │   ├── dashboard/
│   │   └── settings/
│   ├── api/                  # Route Handlers
│   ├── layout.tsx
│   ├── page.tsx
│   └── providers.tsx
├── entities/
├── features/
├── shared/
└── widgets/
```

## Core Patterns

### 1. Server Components (Default)

```typescript
// app/users/page.tsx
// Server Component (기본값)
async function UsersPage() {
  const users = await fetchUsers(); // 서버에서 직접 호출

  return (
    <main>
      <h1>Users</h1>
      <UserList users={users} />
    </main>
  );
}

export default UsersPage;
```

### 2. Client Components

```typescript
// features/theme/ui/theme-toggle.tsx
'use client';

import { useTheme } from 'next-themes';

export const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      Toggle Theme
    </button>
  );
};
```

### 3. Server Actions

```typescript
// features/create-post/api/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // 유효성 검증
  const result = postSchema.safeParse({ title, content });
  if (!result.success) {
    return { error: result.error.flatten() };
  }

  // DB 저장
  await db.post.create({ data: result.data });

  // 캐시 무효화 및 리다이렉트
  revalidatePath('/posts');
  redirect('/posts');
}
```

```typescript
// features/create-post/ui/create-post-form.tsx
'use client';

import { useActionState } from 'react';
import { createPost } from '../api/actions';

export const CreatePostForm = () => {
  const [state, formAction, isPending] = useActionState(createPost, null);

  return (
    <form action={formAction}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      {state?.error && <p className="error">{state.error.formErrors}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
};
```

### 4. Data Fetching Patterns

```typescript
// entities/post/api/queries.ts
import { cache } from 'react';

// React cache로 요청 중복 제거
export const getPost = cache(async (id: string) => {
  const response = await fetch(`${API_URL}/posts/${id}`, {
    next: { revalidate: 60 }, // ISR: 60초
  });
  return response.json();
});

export const getPosts = cache(async () => {
  const response = await fetch(`${API_URL}/posts`, {
    next: { tags: ['posts'] }, // Tag-based revalidation
  });
  return response.json();
});
```

### 5. Parallel & Sequential Data Fetching

```typescript
// app/dashboard/page.tsx
async function DashboardPage() {
  // 병렬 데이터 페칭
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications(),
  ]);

  return (
    <Dashboard
      user={user}
      stats={stats}
      notifications={notifications}
    />
  );
}
```

### 6. Streaming with Suspense

```typescript
// app/posts/[id]/page.tsx
import { Suspense } from 'react';

async function PostPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const post = await getPost(id);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>

      {/* 댓글은 별도로 스트리밍 */}
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments postId={id} />
      </Suspense>
    </article>
  );
}
```

### 7. Route Handlers (API Routes)

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = searchParams.get('page') ?? '1';

  const posts = await getPosts({ page: Number(page) });

  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const result = postSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      { error: result.error.flatten() },
      { status: 400 }
    );
  }

  const post = await createPost(result.data);
  return NextResponse.json(post, { status: 201 });
}
```

### 8. Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');

  // 인증 체크
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*'],
};
```

### 9. Error Handling

```typescript
// app/posts/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}

// app/posts/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Post not found</h2>
      <Link href="/posts">Back to posts</Link>
    </div>
  );
}
```

### 10. Metadata & SEO

```typescript
// app/posts/[id]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const post = await getPost(id);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.thumbnail],
    },
  };
}
```

## Component Guidelines

### Server vs Client Component 결정

| 사용 사례 | 컴포넌트 타입 |
|----------|-------------|
| 데이터 페칭 | Server |
| 백엔드 리소스 직접 접근 | Server |
| 민감한 정보 (API 키 등) | Server |
| 상호작용 (onClick, onChange) | Client |
| 상태 관리 (useState, useReducer) | Client |
| 브라우저 API (localStorage 등) | Client |
| Hooks 사용 | Client |

### Composition Pattern

```typescript
// widgets/post-card/ui/post-card.tsx
// Server Component
async function PostCard({ id }: { id: string }) {
  const post = await getPost(id);

  return (
    <article>
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
      {/* Client Component를 자식으로 */}
      <LikeButton postId={id} initialCount={post.likes} />
    </article>
  );
}
```

## Providers Setup

```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from 'next-themes';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  );
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Best Practices

1. **Server-First**: 기본적으로 Server Component 사용, 필요시에만 'use client'
2. **Colocation**: 데이터 페칭 로직을 사용하는 곳 가까이 배치
3. **Streaming**: Suspense로 점진적 페이지 로딩
4. **Server Actions**: 폼 제출, 뮤테이션은 Server Actions 활용
5. **캐시 전략**: revalidatePath, revalidateTag로 세밀한 캐시 관리
6. **Error Boundaries**: error.tsx, not-found.tsx로 에러 처리

## Anti-Patterns

```typescript
// ❌ Server Component에서 클라이언트 훅 사용
async function Page() {
  const [count, setCount] = useState(0); // Error!
  return <div>{count}</div>;
}

// ❌ 불필요한 'use client'
'use client';
function StaticCard({ title }: { title: string }) {
  return <div>{title}</div>; // 상호작용 없음, Server Component로 충분
}

// ❌ 클라이언트에서 직접 DB 접근
'use client';
async function ClientComponent() {
  const data = await db.query(); // 보안 위험!
}
```

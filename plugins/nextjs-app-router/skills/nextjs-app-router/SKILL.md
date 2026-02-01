---
name: nextjs-app-router
description: Next.js 15+ App Router patterns. Activated when working with Server Components, Server Actions, data fetching, or App Router routing.
---

# Next.js App Router

> Next.js 15+ App Router modern frontend patterns

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
// app/users/page.tsx - Server Component (default)
async function UsersPage() {
  const users = await fetchUsers();

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

  const result = postSchema.safeParse({ title, content });
  if (!result.success) {
    return { error: result.error.flatten() };
  }

  await db.post.create({ data: result.data });

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

### 4. Data Fetching

```typescript
// entities/post/api/queries.ts
import { cache } from 'react';

// React cache for request dedup
export const getPost = cache(async (id: string) => {
  const response = await fetch(`${API_URL}/posts/${id}`, {
    next: { revalidate: 60 }, // ISR: 60s
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

### 5. Parallel Data Fetching

```typescript
// app/dashboard/page.tsx
async function DashboardPage() {
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications(),
  ]);

  return (
    <Dashboard user={user} stats={stats} notifications={notifications} />
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
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments postId={id} />
      </Suspense>
    </article>
  );
}
```

### 7. Route Handlers

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
    return NextResponse.json({ error: result.error.flatten() }, { status: 400 });
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

## Server vs Client Component

|Use Case|Component Type|
|---|---|
|Data fetching|Server|
|Direct backend resource access|Server|
|Sensitive info (API keys)|Server|
|Interactions (onClick, onChange)|Client|
|State management (useState, useReducer)|Client|
|Browser APIs (localStorage)|Client|
|Hooks|Client|

### Composition Pattern

```typescript
// Server Component
async function PostCard({ id }: { id: string }) {
  const post = await getPost(id);

  return (
    <article>
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
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

|Practice|Description|
|---|---|
|Server-First|Default to Server Components, use 'use client' only when needed|
|Colocation|Place data fetching logic close to where it's used|
|Streaming|Use Suspense for progressive page loading|
|Server Actions|Use for form submissions and mutations|
|Cache strategy|Use revalidatePath, revalidateTag for granular cache management|
|Error boundaries|Use error.tsx, not-found.tsx for error handling|

## DO NOT

```typescript
// AVOID: client hooks in Server Component
async function Page() {
  const [count, setCount] = useState(0); // Error!
}

// AVOID: unnecessary 'use client'
'use client';
function StaticCard({ title }: { title: string }) {
  return <div>{title}</div>; // No interaction, Server Component is enough
}

// AVOID: direct DB access from client
'use client';
async function ClientComponent() {
  const data = await db.query(); // Security risk!
}
```

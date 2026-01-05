# Next.js Server Actions Patterns

## Basic Server Action

```typescript
// features/contact/api/actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const contactSchema = z.object({
  name: z.string().min(1, '이름을 입력해주세요'),
  email: z.string().email('올바른 이메일을 입력해주세요'),
  message: z.string().min(10, '메시지는 10자 이상 입력해주세요'),
});

export type ContactState = {
  success?: boolean;
  error?: Record<string, string[]>;
  message?: string;
};

export async function submitContact(
  prevState: ContactState,
  formData: FormData
): Promise<ContactState> {
  const rawData = {
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  };

  const result = contactSchema.safeParse(rawData);

  if (!result.success) {
    return {
      error: result.error.flatten().fieldErrors,
    };
  }

  try {
    await sendEmail(result.data);
    revalidatePath('/contact');

    return {
      success: true,
      message: '문의가 전송되었습니다.',
    };
  } catch (error) {
    return {
      error: { _form: ['전송에 실패했습니다. 다시 시도해주세요.'] },
    };
  }
}
```

## Form Component with useActionState

```typescript
// features/contact/ui/contact-form.tsx
'use client';

import { useActionState } from 'react';
import { submitContact, type ContactState } from '../api/actions';

const initialState: ContactState = {};

export function ContactForm() {
  const [state, formAction, isPending] = useActionState(
    submitContact,
    initialState
  );

  if (state.success) {
    return <div className="success">{state.message}</div>;
  }

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="name">이름</label>
        <input id="name" name="name" required />
        {state.error?.name && (
          <span className="error">{state.error.name[0]}</span>
        )}
      </div>

      <div>
        <label htmlFor="email">이메일</label>
        <input id="email" name="email" type="email" required />
        {state.error?.email && (
          <span className="error">{state.error.email[0]}</span>
        )}
      </div>

      <div>
        <label htmlFor="message">메시지</label>
        <textarea id="message" name="message" required />
        {state.error?.message && (
          <span className="error">{state.error.message[0]}</span>
        )}
      </div>

      {state.error?._form && (
        <div className="error">{state.error._form[0]}</div>
      )}

      <button type="submit" disabled={isPending}>
        {isPending ? '전송 중...' : '문의하기'}
      </button>
    </form>
  );
}
```

## Optimistic Updates

```typescript
// features/like/ui/like-button.tsx
'use client';

import { useOptimistic, useTransition } from 'react';
import { toggleLike } from '../api/actions';

interface Props {
  postId: string;
  initialLiked: boolean;
  initialCount: number;
}

export function LikeButton({ postId, initialLiked, initialCount }: Props) {
  const [isPending, startTransition] = useTransition();
  const [optimistic, setOptimistic] = useOptimistic(
    { liked: initialLiked, count: initialCount },
    (state) => ({
      liked: !state.liked,
      count: state.liked ? state.count - 1 : state.count + 1,
    })
  );

  const handleClick = () => {
    startTransition(async () => {
      setOptimistic(optimistic);
      await toggleLike(postId);
    });
  };

  return (
    <button onClick={handleClick} disabled={isPending}>
      {optimistic.liked ? '❤️' : '🤍'} {optimistic.count}
    </button>
  );
}
```

## File Upload

```typescript
// features/upload/api/actions.ts
'use server';

import { writeFile } from 'fs/promises';
import { join } from 'path';

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File;

  if (!file || file.size === 0) {
    return { error: '파일을 선택해주세요' };
  }

  // 파일 타입 검증
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(file.type)) {
    return { error: '지원하지 않는 파일 형식입니다' };
  }

  // 파일 크기 검증 (5MB)
  if (file.size > 5 * 1024 * 1024) {
    return { error: '파일 크기는 5MB를 초과할 수 없습니다' };
  }

  const bytes = await file.arrayBuffer();
  const buffer = Buffer.from(bytes);

  const filename = `${Date.now()}-${file.name}`;
  const path = join(process.cwd(), 'public/uploads', filename);

  await writeFile(path, buffer);

  return { success: true, url: `/uploads/${filename}` };
}
```

## Delete with Confirmation

```typescript
// features/delete-post/api/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function deletePost(postId: string) {
  await db.post.delete({ where: { id: postId } });

  revalidatePath('/posts');
  redirect('/posts');
}
```

```typescript
// features/delete-post/ui/delete-button.tsx
'use client';

import { useTransition } from 'react';
import { deletePost } from '../api/actions';

export function DeleteButton({ postId }: { postId: string }) {
  const [isPending, startTransition] = useTransition();

  const handleDelete = () => {
    if (!confirm('정말 삭제하시겠습니까?')) return;

    startTransition(() => {
      deletePost(postId);
    });
  };

  return (
    <button onClick={handleDelete} disabled={isPending}>
      {isPending ? '삭제 중...' : '삭제'}
    </button>
  );
}
```

## Inline Server Action

```typescript
// 간단한 경우 인라인으로 정의 가능
async function PostPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const post = await getPost(id);

  async function incrementView() {
    'use server';
    await db.post.update({
      where: { id },
      data: { views: { increment: 1 } },
    });
  }

  // 페이지 로드 시 조회수 증가
  incrementView();

  return <article>{post.content}</article>;
}
```

## Best Practices

1. **유효성 검증**: 항상 서버에서 Zod로 입력값 검증
2. **에러 처리**: 구조화된 에러 응답 반환
3. **낙관적 업데이트**: useOptimistic으로 즉각적 피드백
4. **로딩 상태**: useTransition 또는 useActionState의 isPending 활용
5. **캐시 관리**: 적절한 revalidatePath/revalidateTag 호출

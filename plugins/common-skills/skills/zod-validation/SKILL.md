---
name: zod-validation
description: Zod 스키마 검증 패턴. 폼 검증, API 응답 검증, React Hook Form 통합 시 활성화됩니다.
---

# Zod Validation

> 스키마 검증 - 핵심 패턴만

## 기본 사용

```typescript
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1, '이름을 입력하세요'),
  email: z.string().email('올바른 이메일 형식이 아닙니다'),
  age: z.number().optional(),
});

type User = z.infer<typeof userSchema>;
```

## 폼 검증 (React Hook Form)

```typescript
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  );
}
```

## API 응답 검증

```typescript
const apiResponseSchema = z.object({
  id: z.string(),
  created_at: z.string(),
});

// safeParse: 예외 대신 결과 객체 반환
const result = apiResponseSchema.safeParse(response);

if (!result.success) {
  console.error('Invalid response:', result.error.flatten());
  return null;
}

return result.data;
```

## 자주 쓰는 패턴

### 비밀번호 확인

```typescript
const signupSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: '비밀번호가 일치하지 않습니다',
    path: ['confirmPassword'],
  });
```

### 조건부 필드

```typescript
const schema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('email'), email: z.string().email() }),
  z.object({ type: z.literal('phone'), phone: z.string() }),
]);
```

### 부분 스키마

```typescript
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(),
});

// 생성용 (id 제외)
const createUserSchema = userSchema.omit({ id: true });

// 수정용 (모두 optional + id 필수)
const updateUserSchema = userSchema.partial().required({ id: true });
```

## 그 외는 필요할 때 찾아보세요

Zod 문서가 잘 되어 있습니다. transform, coerce, preprocess 등은 특수한 경우에만 필요합니다.

**핵심**: 타입과 검증을 한 곳에서 관리하고, `z.infer`로 타입 추론하세요.

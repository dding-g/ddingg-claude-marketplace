# Zod Validation Skill

> TypeScript 스키마 선언 및 유효성 검증 가이드

## Overview

Zod는 TypeScript 우선 스키마 선언 및 검증 라이브러리로, 런타임 타입 안전성과 자동 타입 추론을 제공합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- Zod, 스키마, 유효성 검증 언급
- 폼 검증 구현
- API 응답/요청 타입 정의
- DTO 변환 관련

## Core Patterns

### 1. API Schema with DTO

```typescript
// entities/user/model/schema.ts
import { z } from 'zod';

// API 응답 스키마 (snake_case)
export const userResponseSchema = z.object({
  id: z.string().uuid(),
  user_name: z.string(),
  email_address: z.string().email(),
  created_at: z.string().datetime(),
});

// 도메인 스키마 (camelCase)
export const userSchema = userResponseSchema.transform((data) => ({
  id: data.id,
  userName: data.user_name,
  emailAddress: data.email_address,
  createdAt: new Date(data.created_at),
}));

// 타입 추론
export type UserResponse = z.input<typeof userSchema>;
export type User = z.output<typeof userSchema>;
```

### 2. React Hook Form Integration

```typescript
// features/auth/model/schema.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, '이메일을 입력해주세요')
    .email('올바른 이메일 형식이 아닙니다'),
  password: z
    .string()
    .min(1, '비밀번호를 입력해주세요')
    .min(8, '비밀번호는 8자 이상이어야 합니다'),
});

export type LoginFormData = z.infer<typeof loginSchema>;
```

```typescript
// features/auth/ui/login-form.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export const LoginForm = () => {
  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* ... */}
    </form>
  );
};
```

### 3. Conditional Validation (Discriminated Union)

```typescript
export const paymentSchema = z.discriminatedUnion('method', [
  z.object({
    method: z.literal('card'),
    cardNumber: z.string().length(16),
    cvv: z.string().length(3),
    expiryDate: z.string(),
  }),
  z.object({
    method: z.literal('bank'),
    accountNumber: z.string(),
    bankCode: z.string(),
  }),
  z.object({
    method: z.literal('virtual'),
    // 가상계좌는 추가 필드 불필요
  }),
]);
```

### 4. Array and Nested Object

```typescript
export const orderSchema = z.object({
  orderId: z.string(),
  items: z.array(z.object({
    productId: z.string(),
    quantity: z.number().int().positive(),
    price: z.number().nonnegative(),
  })).min(1, '최소 1개 이상의 상품이 필요합니다'),
  shipping: z.object({
    address: z.string().min(1),
    zipCode: z.string().regex(/^\d{5}$/),
  }),
});
```

### 5. Partial Schema (Pick/Omit)

```typescript
// 전체 스키마
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  password: z.string(),
  createdAt: z.date(),
});

// 부분 스키마
const createUserSchema = userSchema.omit({ id: true, createdAt: true });
const updateUserSchema = userSchema.partial().required({ id: true });
const userProfileSchema = userSchema.pick({ name: true, email: true });
```

### 6. Custom Validation (Refinement)

```typescript
const signupSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: '비밀번호가 일치하지 않습니다',
  path: ['confirmPassword'],
});

// 비동기 검증
const usernameSchema = z.string().refine(
  async (username) => {
    const exists = await checkUsernameExists(username);
    return !exists;
  },
  { message: '이미 사용 중인 사용자명입니다' }
);
```

## FSD Integration

```
entities/user/
├── model/
│   ├── schema.ts      # Zod 스키마 정의
│   └── types.ts       # 추론된 타입 export
└── index.ts

features/create-user/
├── model/
│   └── schema.ts      # 폼 검증 스키마
├── ui/
│   └── create-form.tsx
└── index.ts
```

## Error Handling

### Parse (Throwing)

```typescript
try {
  const user = userSchema.parse(data);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error(error.errors);
  }
}
```

### SafeParse (Non-throwing)

```typescript
const result = userSchema.safeParse(data);

if (result.success) {
  const user = result.data;
} else {
  const errors = result.error.flatten();
  // { formErrors: [], fieldErrors: { email: ['...'] } }
}
```

### Error Formatting

```typescript
const formatZodErrors = (error: z.ZodError) => {
  return error.errors.reduce((acc, err) => {
    const path = err.path.join('.');
    acc[path] = err.message;
    return acc;
  }, {} as Record<string, string>);
};
```

## Common Patterns

### Optional vs Nullable

```typescript
// optional: undefined 허용 (필드 생략 가능)
z.string().optional(); // string | undefined

// nullable: null 허용
z.string().nullable(); // string | null

// 둘 다 허용
z.string().nullish(); // string | null | undefined
```

### Default Values

```typescript
const configSchema = z.object({
  theme: z.enum(['light', 'dark']).default('light'),
  pageSize: z.number().default(20),
  notifications: z.boolean().default(true),
});
```

### Coercion

```typescript
// 문자열을 숫자로 변환
z.coerce.number(); // "123" → 123

// 문자열을 날짜로 변환
z.coerce.date(); // "2024-01-01" → Date

// 불리언 변환
z.coerce.boolean(); // "true" → true
```

## Best Practices

1. **DTO와 도메인 분리**: API 응답과 앱 내부 타입을 분리
2. **구체적 에러 메시지**: 사용자 친화적인 메시지 작성
3. **타입 추론 활용**: 스키마에서 타입 추론, 중복 정의 방지
4. **스키마 조합**: extend, merge로 재사용성 높이기
5. **safeParse 선호**: 예외 대신 결과 객체로 처리

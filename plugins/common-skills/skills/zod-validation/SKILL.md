---
name: zod-validation
description: Zod schema validation patterns. Activated when working with form validation, API response validation, or React Hook Form integration.
---

# Zod Validation

> Schema validation - core patterns only

## Basic Usage

```typescript
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email format'),
  age: z.number().optional(),
});

type User = z.infer<typeof userSchema>;
```

## Form Validation (React Hook Form)

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

## API Response Validation

```typescript
const apiResponseSchema = z.object({
  id: z.string(),
  created_at: z.string(),
});

// safeParse: returns result object instead of throwing
const result = apiResponseSchema.safeParse(response);

if (!result.success) {
  console.error('Invalid response:', result.error.flatten());
  return null;
}

return result.data;
```

## Common Patterns

### Password Confirmation

```typescript
const signupSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });
```

### Discriminated Union

```typescript
const schema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('email'), email: z.string().email() }),
  z.object({ type: z.literal('phone'), phone: z.string() }),
]);
```

### Partial Schemas

```typescript
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(),
});

const createUserSchema = userSchema.omit({ id: true });
const updateUserSchema = userSchema.partial().required({ id: true });
```

|Principle|Description|
|---|---|
|Single source of truth|Type and validation in one place via `z.infer`|
|safeParse for APIs|Use safeParse at system boundaries|
|Keep it simple|transform, coerce, preprocess only when truly needed|

---
name: typescript-patterns
description: Practical TypeScript patterns. Activated when working with type inference, utility types, generics, type guards, or type narrowing.
---

# TypeScript Patterns

> Practical type authoring patterns

## Type Inference

```typescript
// AVOID: unnecessary type annotations
const name: string = 'John';
const items: string[] = ['a', 'b', 'c'];

// PREFER: let inference work
const name = 'John';
const items = ['a', 'b', 'c'];
```

**When to annotate**: function parameters, complex return types, exported types

## Utility Types

```typescript
type UpdateUser = Partial<User>;                    // All optional
type UserPreview = Pick<User, 'id' | 'name'>;      // Pick subset
type CreateUser = Omit<User, 'id' | 'createdAt'>;  // Exclude fields
type RequiredConfig = Required<Config>;              // All required
type UserMap = Record<string, User>;                 // Key-value map

// Combinations
type UpdateUser = Partial<User> & { id: string };           // id required, rest optional
type CreateUser = Omit<User, 'id'> & { id?: string };      // specific field optional
```

## Narrowing

### typeof, in, instanceof

```typescript
function process(input: string | number) {
  if (typeof input === 'string') {
    return input.toUpperCase();
  }
  return input.toFixed(2);
}

function handleResponse(res: SuccessResponse | ErrorResponse) {
  if ('error' in res) {
    console.error(res.error);
    return;
  }
  return res.data;
}
```

### Discriminated Union (Recommended)

```typescript
type Result =
  | { status: 'success'; data: User }
  | { status: 'error'; error: Error }
  | { status: 'loading' };

function handleResult(result: Result) {
  switch (result.status) {
    case 'success':
      return result.data;
    case 'error':
      throw result.error;
    case 'loading':
      return null;
  }
}
```

### Custom Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

const data: unknown = await fetchData();
if (isUser(data)) {
  console.log(data.name);
}
```

## Generics

```typescript
// API response wrapper
interface ApiResponse<T> {
  data: T;
  status: number;
}

// Generic constraint
function findById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Component generic
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

## as const

```typescript
const ROUTES = {
  HOME: '/',
  ABOUT: '/about',
  USER: '/user',
} as const;

type Route = typeof ROUTES[keyof typeof ROUTES]; // '/' | '/about' | '/user'

const STATUSES = ['pending', 'active', 'done'] as const;
type Status = typeof STATUSES[number]; // 'pending' | 'active' | 'done'
```

## DO NOT

```typescript
// AVOID: any
function process(data: any) { ... }
// USE: unknown + type guard
function process(data: unknown) {
  if (isValidData(data)) { ... }
}

// AVOID: type assertion abuse
const user = data as User;
// USE: type guard
if (isUser(data)) { const user = data; }

// AVOID: non-null assertion overuse
const name = user!.name!;
// USE: optional chaining + nullish coalescing
const name = user?.name ?? 'Unknown';

// AVOID: enum (not tree-shakeable)
enum Status { Active, Inactive }
// USE: as const + union
const Status = { Active: 'active', Inactive: 'inactive' } as const;
type Status = typeof Status[keyof typeof Status];
```

## Practical Tips

```typescript
// Component Props type
type ButtonProps = React.ComponentProps<'button'> & {
  variant?: 'primary' | 'secondary';
};

// Event handler type
const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
  setValue(e.target.value);
};

// Promise return type
async function fetchUser(id: string): Promise<User> {
  const response = await api.get(`/users/${id}`);
  return response.data;
}
```

|Principle|Description|
|---|---|
|Types are docs|Express intent clearly, don't overcomplicate|
|Infer first|Only annotate when inference falls short|
|unknown > any|Always prefer unknown with guards|

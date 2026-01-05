# FSD Architecture Skill

> Feature-Sliced Design 아키텍처 설계 및 구현 가이드

## Overview

FSD는 프론트엔드 프로젝트를 위한 현대적인 아키텍처 방법론으로, 코드를 표준화된 레이어와 슬라이스로 구성합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- FSD, Feature-Sliced Design 언급
- 아키텍처 구조 관련 질문
- 폴더 구조 설계 요청
- 레이어/슬라이스 생성 요청

## Capabilities

1. **구조 생성**: FSD 폴더 레이아웃 생성
2. **의존성 검증**: 레이어 간 의존성 규칙 검증
3. **슬라이스 관리**: 보일러플레이트 코드 생성
4. **베스트 프랙티스**: FSD 원칙 적용

## Layer Hierarchy

```
app/        → 앱 초기화, 프로바이더, 라우팅
pages/      → 전체 페이지, 라우트 컴포넌트
widgets/    → 독립적인 UI 블록 조합
features/   → 사용자 시나리오, 비즈니스 로직
entities/   → 비즈니스 엔티티 (User, Product 등)
shared/     → 재사용 유틸리티, UI Kit
```

## Dependency Rules

```
app     → pages, widgets, features, entities, shared
pages   → widgets, features, entities, shared
widgets → features, entities, shared
features → entities, shared
entities → shared
shared   → (외부 라이브러리만)
```

**핵심 원칙**: 상위 레이어는 하위 레이어만 import 가능 (단방향)

## Slice Structure

각 슬라이스는 다음 세그먼트를 포함할 수 있습니다:

```
features/auth/
├── ui/           # React 컴포넌트
├── model/        # 상태, 스토어, 타입
├── api/          # API 호출, React Query
├── lib/          # 유틸리티 함수
├── config/       # 상수, 설정
└── index.ts      # Public API
```

## Public API Pattern

모든 import는 반드시 index.ts를 통해야 합니다:

```typescript
// ✅ Good - Public API 사용
import { LoginForm } from '@/features/auth';
import { useUser } from '@/entities/user';

// ❌ Bad - 내부 구조 직접 접근
import { LoginForm } from '@/features/auth/ui/login-form';
import { useUser } from '@/entities/user/model/hooks';
```

## Templates

### Entity Slice

```typescript
// entities/user/model/types.ts
export interface User {
  id: string;
  email: string;
  name: string;
}

// entities/user/api/queries.ts
export const userKeys = {
  all: ['users'] as const,
  detail: (id: string) => [...userKeys.all, id] as const,
};

export const userQueries = {
  detail: (id: string) => queryOptions({
    queryKey: userKeys.detail(id),
    queryFn: () => api.get<User>(`/users/${id}`),
  }),
};

// entities/user/index.ts
export type { User } from './model/types';
export { userKeys, userQueries } from './api/queries';
```

### Feature Slice

```typescript
// features/auth/ui/login-form.tsx
export const LoginForm = () => {
  const { mutate: login } = useLoginMutation();
  // ...
};

// features/auth/api/mutations.ts
export const useLoginMutation = () => {
  return useMutation({
    mutationFn: (credentials: LoginCredentials) =>
      api.post('/auth/login', credentials),
  });
};

// features/auth/index.ts
export { LoginForm } from './ui/login-form';
export { useLoginMutation } from './api/mutations';
```

## Naming Conventions

| 대상 | 컨벤션 | 예시 |
|------|--------|------|
| Layers | lowercase | `features`, `entities` |
| Slices | kebab-case | `user-profile`, `shopping-cart` |
| Components | PascalCase | `LoginForm.tsx` |
| Hooks | camelCase | `useAuth.ts` |
| Utils | kebab-case | `format-date.ts` |

## Troubleshooting

### 순환 참조 해결

```typescript
// ❌ 순환 참조 발생
// features/auth → entities/user → features/auth

// ✅ 해결: shared로 공통 타입 이동
// shared/types/user.ts
export interface BaseUser { ... }
```

### tsconfig paths 설정

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/shared/*": ["./src/shared/*"],
      "@/entities/*": ["./src/entities/*"],
      "@/features/*": ["./src/features/*"],
      "@/widgets/*": ["./src/widgets/*"],
      "@/pages/*": ["./src/pages/*"]
    }
  }
}
```

## Best Practices

1. **슬라이스 독립성**: 같은 레이어의 슬라이스끼리 import 금지
2. **Public API 강제**: 반드시 index.ts를 통한 export
3. **세그먼트 분리**: ui, model, api, lib 명확히 구분
4. **네이밍 일관성**: kebab-case 슬라이스, PascalCase 컴포넌트

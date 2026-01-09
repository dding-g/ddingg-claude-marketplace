---
name: fsd-architecture
description: Feature-Sliced Design 아키텍처 패턴. FSD, 레이어, 슬라이스, 의존성 규칙 관련 코드 작성 시 활성화됩니다.
---

# FSD Architecture

> Feature-Sliced Design - 프론트엔드 표준 아키텍처

## 레이어 구조

```
src/
├── app/        # 앱 초기화, providers, router, global styles
├── pages/      # 라우트 진입점 (조합만, 로직 X)
├── widgets/    # 독립적인 UI 블록 조합
├── features/   # 사용자 액션 (로그인, 좋아요, 댓글 작성)
├── entities/   # 비즈니스 엔티티 (User, Product, Order)
└── shared/     # 공용 유틸, UI Kit, API 클라이언트
```

## 의존성 규칙 (필수)

```
app     → pages, widgets, features, entities, shared
pages   → widgets, features, entities, shared
widgets → features, entities, shared
features → entities, shared
entities → shared
shared   → (외부 라이브러리만)
```

**위에서 아래로만 import 가능. 예외 없음.**

```typescript
// ✅ 허용
// features/auth/ui/login-form.tsx
import { User } from '@/entities/user';
import { Button } from '@/shared/ui';

// ❌ 금지 - 상위 레이어 import
// entities/user/model/hooks.ts
import { useAuth } from '@/features/auth';  // 절대 안됨

// ❌ 금지 - 같은 레이어 내 다른 슬라이스 import
// features/auth/ui/login-form.tsx
import { useProfile } from '@/features/profile';  // 절대 안됨
```

## 슬라이스 구조

```
features/auth/
├── ui/              # 컴포넌트
│   ├── login-form.tsx
│   └── logout-button.tsx
├── model/           # 상태, 타입
│   ├── types.ts
│   └── store.ts
├── api/             # API 호출, React Query
│   ├── queries.ts
│   └── mutations.ts
├── lib/             # 유틸리티
│   └── validate-token.ts
└── index.ts         # Public API (필수)
```

## Public API (필수)

모든 슬라이스는 반드시 `index.ts`를 통해 export 합니다.

```typescript
// features/auth/index.ts
export { LoginForm } from './ui/login-form';
export { LogoutButton } from './ui/logout-button';
export { useLoginMutation } from './api/mutations';
export type { LoginCredentials } from './model/types';
```

```typescript
// ✅ 올바른 import
import { LoginForm, useLoginMutation } from '@/features/auth';

// ❌ 금지 - 내부 구조 직접 접근
import { LoginForm } from '@/features/auth/ui/login-form';
```

## 레이어별 역할

### app/
- Provider 설정 (QueryClient, Theme, Auth)
- 글로벌 스타일
- 라우터 설정

### pages/
- 라우트 진입점
- 위젯/피처 조합만 (비즈니스 로직 X)
- 페이지별 레이아웃

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

### widgets/
- 독립적인 UI 블록
- features, entities 조합
- 페이지에 바로 배치 가능한 단위

```typescript
// widgets/user-profile/index.tsx
export function UserProfile({ userId }: Props) {
  const { data: user } = useUser(userId);        // entities
  const { mutate: follow } = useFollowMutation(); // features

  return (
    <Card>
      <UserAvatar user={user} />
      <UserInfo user={user} />
      <FollowButton onFollow={() => follow(userId)} />
    </Card>
  );
}
```

### features/
- 사용자 액션 단위
- 비즈니스 로직 포함
- Mutation 위치

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

### entities/
- 비즈니스 엔티티
- 타입 정의
- Query 위치 (읽기 전용)

```typescript
// entities/user/api/queries.ts
export const userQueries = {
  detail: (id: string) => queryOptions({
    queryKey: ['user', id],
    queryFn: () => api.get<User>(`/users/${id}`),
  }),
};

// entities/user/index.ts
export type { User } from './model/types';
export { userQueries } from './api/queries';
export { useUser } from './api/hooks';
```

### shared/
- 프로젝트 독립적인 코드
- UI Kit (Button, Input, Modal)
- 유틸리티 함수
- API 클라이언트

```
shared/
├── ui/           # 공통 UI 컴포넌트
├── api/          # API 클라이언트, 인터셉터
├── lib/          # 유틸리티 (date, format)
├── config/       # 상수, 환경변수
└── types/        # 공통 타입
```

## 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 레이어 | lowercase | `features`, `entities` |
| 슬라이스 | kebab-case | `user-profile`, `create-post` |
| 컴포넌트 파일 | kebab-case | `login-form.tsx` |
| 컴포넌트 | PascalCase | `LoginForm` |
| 훅 | camelCase | `useUser`, `useLoginMutation` |
| 타입 | PascalCase | `User`, `LoginCredentials` |

## tsconfig paths 설정

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

## 순환 참조 해결

순환 참조가 발생하면 공통 타입을 `shared`로 이동:

```typescript
// ❌ 순환 참조
// entities/user → entities/post → entities/user

// ✅ 해결: shared로 분리
// shared/types/index.ts
export interface BaseUser { id: string; name: string; }
export interface BasePost { id: string; authorId: string; }
```

## 체크리스트

새 코드 작성 시 확인:

- [ ] 올바른 레이어에 배치했는가?
- [ ] 상위 레이어를 import하지 않았는가?
- [ ] 같은 레이어의 다른 슬라이스를 import하지 않았는가?
- [ ] index.ts를 통해 export 했는가?
- [ ] 네이밍 컨벤션을 따랐는가?

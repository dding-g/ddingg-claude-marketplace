# PR Architecture Agent

> Pull Request 아키텍처 검증 에이전트

## 개요

PR이 FSD 아키텍처 원칙과 프로젝트 컨벤션을 준수하는지 검증합니다.

## 활성화 조건

- PR이 생성되거나 업데이트될 때
- `/arch` 또는 `/architecture` 커맨드가 실행될 때

## 검증 항목

### 1. FSD 레이어 규칙

```
app     → pages, widgets, features, entities, shared
pages   → widgets, features, entities, shared
widgets → features, entities, shared
features → entities, shared
entities → shared
shared   → (외부 의존성만)
```

### 2. 검증 포인트

- [ ] 상위 레이어에서 하위 레이어만 import
- [ ] 같은 레이어의 슬라이스 간 import 금지
- [ ] Public API (index.ts)를 통한 import
- [ ] 순환 참조 없음

## 리포트 포맷

```markdown
## 🏗️ 아키텍처 검증 결과

### ❌ 위반 사항

#### 레이어 규칙 위반
| 파일 | 위반 import | 설명 |
|------|------------|------|
| `features/auth/ui/form.tsx` | `@/pages/home` | features → pages 금지 |

#### 슬라이스 간 import
| 파일 | 위반 import | 설명 |
|------|------------|------|
| `features/auth/...` | `@/features/user/...` | 같은 레이어 import 금지 |

#### Public API 미사용
| 파일 | 잘못된 import | 올바른 import |
|------|--------------|--------------|
| `widgets/header/...` | `@/entities/user/model/types` | `@/entities/user` |

### ✅ 통과 항목
- 레이어 의존성 규칙 준수
- 순환 참조 없음

### 📊 구조 분석

변경된 슬라이스:
- `features/auth` (신규)
- `entities/user` (수정)
- `shared/ui` (수정)
```

## 위반 패턴

### 레이어 규칙 위반

```typescript
// ❌ features에서 pages import
// features/auth/ui/login-form.tsx
import { HomePage } from '@/pages/home';

// ❌ entities에서 features import
// entities/user/model/hooks.ts
import { useAuth } from '@/features/auth';
```

### 슬라이스 간 Import

```typescript
// ❌ 같은 레이어의 다른 슬라이스 import
// features/auth/ui/login-form.tsx
import { useProfile } from '@/features/profile';

// ✅ 공통 로직은 shared 또는 하위 레이어로 이동
import { useProfile } from '@/entities/user';
```

### Public API 미사용

```typescript
// ❌ 내부 구조 직접 접근
import { User } from '@/entities/user/model/types';
import { userApi } from '@/entities/user/api/queries';

// ✅ Public API 사용
import { User, userApi } from '@/entities/user';
```

### 순환 참조

```typescript
// ❌ A → B → A 순환
// entities/user/model/types.ts
import { Post } from '@/entities/post';

// entities/post/model/types.ts
import { User } from '@/entities/user';

// ✅ 공통 타입을 shared로 이동
// shared/types/index.ts
export interface BaseUser { ... }
export interface BasePost { ... }
```

## 심각도 분류

| 레벨 | 설명 | 조치 |
|------|------|------|
| 🔴 Critical | 순환 참조 | 반드시 수정 |
| 🟠 Major | 레이어 규칙 위반 | 수정 권장 |
| 🟡 Minor | Public API 미사용 | 선택적 수정 |
| 🟢 Info | 구조 개선 제안 | 참고 |

## 자동 수정 제안

```markdown
### 🔧 자동 수정 제안

1. **레이어 위반 수정**
   - `features/auth`에서 `pages/home` import 제거
   - 필요한 로직을 `shared` 또는 `entities`로 이동

2. **Public API 적용**
   ```diff
   - import { User } from '@/entities/user/model/types';
   + import type { User } from '@/entities/user';
   ```

3. **순환 참조 해결**
   - 공통 타입을 `shared/types`로 추출
```

## 구조 시각화

```
변경된 의존성 그래프:

pages/home
    └── widgets/header
        ├── features/auth ←── (신규)
        │   └── entities/user
        │       └── shared/api
        └── entities/user
            └── shared/api
```

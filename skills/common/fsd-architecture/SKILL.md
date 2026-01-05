# FSD Architecture

> Feature-Sliced Design - 언제, 왜 사용하는가

## 핵심 개념

FSD는 **도메인 중심**으로 코드를 구성하는 방법론입니다.

```
app/        # 앱 설정 (providers, router)
pages/      # 라우트 진입점
widgets/    # 페이지 조합 블록
features/   # 사용자 액션 (로그인, 좋아요, 댓글 작성)
entities/   # 도메인 모델 (User, Product, Order)
shared/     # 공용 유틸, UI 컴포넌트
```

**의존성 규칙**: 위에서 아래로만 import 가능

## 언제 FSD를 사용할까?

### 적합한 경우
- 3명 이상 협업하는 중규모 이상 프로젝트
- 명확한 도메인 경계가 있는 서비스
- 장기 유지보수가 필요한 프로젝트

### 부적합한 경우
- MVP, 프로토타입, 1인 개발
- 도메인이 모호한 유틸리티 앱
- 빠른 실험이 필요한 초기 스타트업

**FSD가 부담스럽다면 단순화하세요:**

```
src/
├── components/    # 공통 UI
├── features/      # 기능 단위 (폴더 하나에 관련 코드 모두)
├── hooks/         # 공통 훅
├── lib/           # 유틸리티
└── pages/         # 라우트
```

## 실용적 적용

### 1. 슬라이스 = 관련 코드를 한 곳에

```
features/auth/
├── login-form.tsx       # 컴포넌트
├── use-login.ts         # 훅
├── schema.ts            # 유효성 검증
├── types.ts             # 타입
└── index.ts             # Public API
```

폴더 구조보다 **관련 코드가 함께 있는 것**이 중요합니다.

### 2. index.ts는 선택사항

```typescript
// 팀이 동의하면 직접 import도 OK
import { LoginForm } from '@/features/auth/login-form';

// index.ts를 통한 import
import { LoginForm } from '@/features/auth';
```

index.ts 강제보다 **일관성**이 중요합니다.

### 3. 레이어 위반? 상황에 따라 판단

```typescript
// "규칙상" features끼리 import 금지
// 하지만 실용적으로 필요하다면?

// features/checkout/index.ts
import { useCart } from '@/features/cart';  // 허용할 수도 있음

// 대안: 공통 로직을 entities로 내리기
import { useCartItems } from '@/entities/cart';
```

## 핵심 원칙 3가지

1. **함께 변경되는 코드는 함께 둔다**
2. **의존 방향을 일관되게 유지한다** (가능하면 단방향)
3. **팀이 이해하고 따를 수 있어야 한다**

아키텍처는 도구입니다. 팀에 맞게 조정하세요.

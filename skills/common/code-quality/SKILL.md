# Code Quality Skill

> Toss Frontend Fundamentals 기반 코드 품질 개선 가이드

## Overview

5가지 핵심 원칙을 기반으로 코드 품질을 분석하고 개선합니다.

## Activation

다음 상황에서 이 스킬이 활성화됩니다:

- 코드 리뷰 요청
- 리팩토링 제안 요청
- SOLID 원칙 검사
- 컴포넌트 복잡도 분석
- "이 코드 괜찮아?" 류의 질문

## 5 Core Principles

### 1. 가독성 (Readability)

복잡한 로직도 이해할 수 있어야 변경이 가능합니다.

```typescript
// ❌ Bad
const x = a ? (b ? c : d) : e ? f : g;

// ✅ Good
const getResult = () => {
  if (a && b) return c;
  if (a) return d;
  if (e) return f;
  return g;
};
```

### 2. 예측 가능성 (Predictability)

동료들이 함수의 동작을 쉽게 예측할 수 있어야 합니다.

```typescript
// ❌ Bad - 이름과 다른 동작
const getUser = async (id: string) => {
  const user = await fetchUser(id);
  analytics.track('user_viewed'); // 숨겨진 사이드 이펙트
  return user;
};

// ✅ Good
const getUser = async (id: string) => {
  return fetchUser(id);
};

const trackUserView = () => {
  analytics.track('user_viewed');
};
```

### 3. 응집도 (Cohesion)

함께 수정되는 코드는 같은 곳에 있어야 합니다.

```typescript
// ❌ Bad - 관련 코드가 분산됨
// constants/status.ts
export const STATUS = { ACTIVE: 'active', INACTIVE: 'inactive' };

// utils/status.ts
export const getStatusLabel = (status: string) => { ... };

// components/StatusBadge.tsx
import { STATUS } from '../constants/status';
import { getStatusLabel } from '../utils/status';

// ✅ Good - 관련 코드를 함께 배치
// components/StatusBadge/index.tsx
const STATUS = { ACTIVE: 'active', INACTIVE: 'inactive' } as const;
const getStatusLabel = (status: Status) => { ... };

export const StatusBadge = ({ status }: Props) => { ... };
```

### 4. 결합도 (Coupling)

수정 시 영향 범위를 최소화해야 합니다.

```typescript
// ❌ Bad - 높은 결합도
const UserProfile = ({ user }: { user: ComplexUserObject }) => {
  return <div>{user.profile.personal.name}</div>;
};

// ✅ Good - 낮은 결합도
const UserProfile = ({ name }: { name: string }) => {
  return <div>{name}</div>;
};
```

### 5. 추상화 (Abstraction)

의미 있는 추상화로 복잡도를 감소시킵니다.

```typescript
// ❌ Bad - 과도한 추상화
const Button = ({
  variant, size, color, disabled, loading,
  leftIcon, rightIcon, fullWidth, ...rest
}: ButtonProps) => { ... };

// ✅ Good - 적절한 추상화
const PrimaryButton = (props: BaseButtonProps) => { ... };
const SecondaryButton = (props: BaseButtonProps) => { ... };
const IconButton = (props: IconButtonProps) => { ... };
```

## Quality Metrics

| 지표 | 권장 기준 |
|------|----------|
| 컴포넌트 라인 수 | ≤ 250줄 |
| useEffect 개수 | ≤ 3개 |
| useState 개수 | ≤ 5개 |
| Props Drilling 깊이 | ≤ 3단계 |
| Props 개수 | ≤ 7개 |
| Cyclomatic Complexity | ≤ 10 |

## Analysis Checklist

### Component Analysis

- [ ] 단일 책임 원칙 준수 여부
- [ ] Props 개수 적절성 (7개 이하)
- [ ] 조건부 렌더링 복잡도
- [ ] 훅 사용 패턴 적절성

### Function Analysis

- [ ] 함수명과 동작 일치
- [ ] 순수 함수 여부
- [ ] 매개변수 개수 (3개 이하 권장)
- [ ] 반환 타입 일관성

### State Management

- [ ] 상태 위치 적절성
- [ ] 불필요한 상태 여부
- [ ] 파생 상태 사용 여부

## Refactoring Suggestions

### Extract Component

```typescript
// Before
const UserCard = ({ user }) => (
  <div>
    <img src={user.avatar} alt="" />
    <div>{user.name}</div>
    <div>{user.email}</div>
    <button onClick={() => follow(user.id)}>Follow</button>
    <button onClick={() => message(user.id)}>Message</button>
  </div>
);

// After
const UserCard = ({ user }) => (
  <div>
    <UserAvatar user={user} />
    <UserInfo user={user} />
    <UserActions userId={user.id} />
  </div>
);
```

### Extract Custom Hook

```typescript
// Before
const Component = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData().then(setData).catch(setError).finally(() => setLoading(false));
  }, []);

  // ...
};

// After
const Component = () => {
  const { data, isLoading, error } = useData();
  // ...
};
```

## Philosophy

> "완벽한 코드보다 점진적 개선"

- 한 번에 모든 것을 고치려 하지 않기
- 실용적이고 증분적인 개선 우선
- 팀 컨벤션과 일관성 유지

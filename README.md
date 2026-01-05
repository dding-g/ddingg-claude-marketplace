# Frontend Claude Settings

프론트엔드 개발 환경을 위한 Claude 스킬 및 에이전트 모음입니다.

## 📁 구조

```
.
├── skills/
│   ├── common/                    # 공통 스킬
│   │   ├── fsd-architecture/      # FSD 아키텍처 가이드
│   │   ├── react-query-patterns/  # React Query 패턴
│   │   ├── zod-validation/        # Zod 유효성 검증
│   │   ├── code-quality/          # 코드 품질 가이드
│   │   └── code-smell/            # 코드 스멜 탐지
│   │
│   ├── nextjs-app-router/         # Next.js App Router 스킬
│   │   ├── SKILL.md
│   │   └── patterns/
│   │       ├── data-fetching.md
│   │       └── server-actions.md
│   │
│   ├── vite-csr/                  # Vite CSR 프로젝트 스킬
│   │   ├── SKILL.md
│   │   └── patterns/
│   │       ├── routing.md
│   │       └── state-management.md
│   │
│   └── react-native/              # React Native 스킬
│       ├── SKILL.md
│       └── patterns/
│           ├── navigation.md
│           ├── performance.md
│           └── native-features.md
│
└── agents/                        # PR 에이전트
    ├── pr-review.md               # PR 리뷰 에이전트
    ├── pr-summary.md              # PR 요약 에이전트
    ├── pr-test-check.md           # 테스트 검증 에이전트
    ├── pr-security.md             # 보안 검증 에이전트
    └── pr-architecture.md         # 아키텍처 검증 에이전트
```

## 🎯 지원 환경

| 환경 | 설명 |
|------|------|
| **Next.js App Router** | Next.js 15+ App Router 기반 SSR/SSG 프로젝트 |
| **Vite CSR** | Vite 기반 React SPA/CSR 프로젝트 |
| **React Native** | Expo Router 기반 모바일 앱 프로젝트 |

## 📚 공통 스킬

### FSD Architecture
Feature-Sliced Design 아키텍처 구현 가이드

### React Query Patterns
TanStack Query를 활용한 서버 상태 관리 패턴

### Zod Validation
TypeScript 스키마 선언 및 유효성 검증

### Code Quality
Toss Frontend Fundamentals 기반 코드 품질 가이드

### Code Smell
코드 스멜 탐지 및 리팩토링 가이드

## 🤖 PR 에이전트

| 에이전트 | 설명 | 커맨드 |
|---------|------|--------|
| **PR Review** | 코드 품질, 보안, 성능 리뷰 | `/review` |
| **PR Summary** | 변경사항 요약 생성 | `/summary` |
| **Test Check** | 테스트 커버리지 검증 | `/test-check` |
| **Security** | 보안 취약점 분석 | `/security` |
| **Architecture** | FSD 아키텍처 검증 | `/arch` |

## 🚀 사용법

### 스킬 활성화

스킬은 관련 키워드가 감지되면 자동으로 활성화됩니다:

- "FSD", "Feature-Sliced Design" → FSD Architecture 스킬
- "React Query", "useQuery" → React Query Patterns 스킬
- "Zod", "스키마", "검증" → Zod Validation 스킬
- "App Router", "Server Actions" → Next.js App Router 스킬
- "React Native", "Expo" → React Native 스킬

### PR 에이전트 실행

PR 코멘트에서 커맨드를 입력하여 에이전트를 실행합니다:

```
/review      # 전체 코드 리뷰
/summary     # 변경사항 요약
/security    # 보안 검사
/arch        # 아키텍처 검증
/test-check  # 테스트 검증
```

## 📝 컨벤션

- **파일명**: kebab-case 사용 (`user-profile.tsx`)
- **컴포넌트명**: PascalCase 사용 (`UserProfile`)
- **훅명**: camelCase + use 접두사 (`useUserProfile`)
- **상수명**: SCREAMING_SNAKE_CASE (`MAX_RETRY_COUNT`)

## 🔗 참고 자료

- [Feature-Sliced Design](https://feature-sliced.design/)
- [TanStack Query](https://tanstack.com/query)
- [Zod Documentation](https://zod.dev/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Expo Documentation](https://docs.expo.dev/)

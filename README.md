# Frontend Claude Settings

프론트엔드 개발을 위한 Claude 스킬 및 에이전트

## 📁 구조

```
skills/
├── common/                       # 공통 스킬
│   ├── writing-good-code/        # 좋은 코드 작성법
│   ├── typescript-patterns/      # TypeScript 실용 패턴
│   ├── react-patterns/           # Modern React 패턴
│   ├── fsd-architecture/         # FSD 아키텍처 (실용적 가이드)
│   ├── react-query-patterns/     # React Query (심플하게)
│   └── zod-validation/           # Zod 검증 (핵심만)
│
├── nextjs-app-router/            # Next.js 15+ App Router
├── vite-csr/                     # Vite CSR/SPA
└── react-native/                 # React Native/Expo

agents/                           # PR 에이전트
├── pr-review.md
├── pr-summary.md
├── pr-test-check.md
├── pr-security.md
└── pr-architecture.md
```

## 철학

- **심플하게 시작, 필요할 때 확장**
- 교과서적 규칙보다 **실용적 판단**
- 과도한 추상화보다 **명확한 코드**
- 트렌드 추종보다 **문제 해결**

## 스킬 개요

### Common Skills

| 스킬 | 핵심 내용 |
|------|----------|
| **writing-good-code** | 이름 짓기, 함수 분리, 조건문, Early Return |
| **typescript-patterns** | 타입 추론, 유틸리티 타입, 제네릭, 타입 좁히기 |
| **react-patterns** | 상태 관리 판단, Suspense, React 19 패턴 |
| **fsd-architecture** | 언제 FSD를 쓸까? 실용적 적용법 |
| **react-query-patterns** | 기본 Query/Mutation, 필요시에만 확장 |
| **zod-validation** | 폼 검증, API 응답 검증, 핵심 패턴 3가지 |

### Platform Skills

| 스킬 | 대상 |
|------|------|
| **nextjs-app-router** | Server Components, Server Actions, 데이터 페칭 |
| **vite-csr** | React Router, Zustand, 코드 스플리팅 |
| **react-native** | Expo Router, 네이티브 기능, 성능 최적화 |

## PR 에이전트

| 에이전트 | 역할 | 커맨드 |
|---------|------|--------|
| **PR Review** | 코드 품질, 보안, 성능 | `/review` |
| **PR Summary** | 변경사항 요약 | `/summary` |
| **Test Check** | 테스트 커버리지 | `/test-check` |
| **Security** | 보안 취약점 | `/security` |
| **Architecture** | FSD 아키텍처 검증 | `/arch` |

## 사용법

스킬은 관련 키워드 감지 시 자동 활성화됩니다.

PR 에이전트는 코멘트에서 커맨드로 실행:
```
/review
/summary
/security
```

## 컨벤션

- 파일명: `kebab-case`
- 컴포넌트: `PascalCase`
- 훅: `useCamelCase`
- 상수: `SCREAMING_SNAKE_CASE`

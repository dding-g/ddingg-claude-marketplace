# Marketplace Development Skill

> 이 마켓플레이스 프로젝트를 개발/유지보수하기 위한 스킬

## Overview

frontend-claude-settings 마켓플레이스의 스킬과 에이전트를 생성, 수정, 관리하는 방법에 대한 지식을 제공합니다.

## Activation

다음 상황에서 활성화됩니다:
- skills/ 또는 agents/ 디렉토리 파일 작업 시
- 새 스킬이나 에이전트 생성 요청 시
- 마켓플레이스 구조 수정 시
- 플러그인 설정 변경 시

## 프로젝트 구조

```
ddingg-claude-marketplace/
├── .claude-plugin/
│   └── plugin.json           # 플러그인 매니페스트
│
├── .claude/                   # 프로젝트 로컬 설정
│   ├── settings.local.json   # 권한 설정
│   ├── commands/             # 프로젝트 관리 명령어
│   │   ├── add-skill.md
│   │   ├── add-agent.md
│   │   ├── validate-structure.md
│   │   └── generate-readme.md
│   └── skills/
│       └── marketplace-dev/  # 이 스킬
│
├── agents/                    # PR 에이전트 (배포용)
│   ├── pr-architecture.md
│   ├── pr-review.md
│   ├── pr-security.md
│   ├── pr-summary.md
│   └── pr-test-check.md
│
├── skills/                    # 프론트엔드 스킬 (배포용)
│   ├── common/               # 공통 스킬
│   │   ├── fsd-architecture/
│   │   ├── react-patterns/
│   │   ├── react-query-patterns/
│   │   ├── typescript-patterns/
│   │   ├── writing-good-code/
│   │   └── zod-validation/
│   ├── nextjs-app-router/    # Next.js 스킬
│   ├── react-native/         # React Native 스킬
│   └── vite-csr/             # Vite SPA 스킬
│
├── hooks/
│   └── hooks.json            # 품질 관리 훅
│
├── README.md
└── CONTRIBUTING.md
```

## SKILL.md 작성 규칙

### 필수 섹션

```markdown
# Skill Name

> 한 줄 설명 (필수)

## Overview
스킬의 목적과 범위

## Activation
활성화 트리거 (키워드, 상황)

## Core Patterns
코드 예제와 패턴
```

### 권장 섹션

```markdown
## Best Practices
권장 사항

## Anti-Patterns
피해야 할 패턴
```

### 코드 예제 형식

```typescript
// ❌ Bad - 나쁜 예제
const d = new Date().getTime() - startTime;

// ✅ Good - 좋은 예제
const elapsedMs = new Date().getTime() - startTime;
const TIMEOUT_MS = 3000;
```

## Agent 작성 규칙

### 파일 위치

```bash
agents/pr-<name>.md
```

### 필수 섹션

```markdown
# PR <Name> Agent

> 에이전트 설명

## 개요
## 활성화 조건
## 체크리스트
```

### 권장 섹션

```markdown
## 리포트 포맷
## 심각도 레벨
## 자동 체크 항목
```

## 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 디렉토리 | kebab-case | `react-patterns` |
| 스킬 파일 | SKILL.md (대문자) | `SKILL.md` |
| 에이전트 파일 | pr-<name>.md | `pr-review.md` |
| 패턴 파일 | kebab-case.md | `data-fetching.md` |

## 스킬 카테고리

| 카테고리 | 위치 | 용도 |
|----------|------|------|
| common | skills/common/ | 프레임워크 독립적 |
| platform | skills/<platform>/ | 플랫폼 특화 |

현재 플랫폼:
- `nextjs-app-router`: Next.js 15+ App Router
- `vite-csr`: Vite + React SPA
- `react-native`: React Native / Expo

## 품질 체크리스트

### 스킬 추가/수정 시

- [ ] SKILL.md에 필수 섹션 포함
- [ ] 코드 예제가 문법적으로 올바름
- [ ] 좋은/나쁜 예제 모두 포함
- [ ] 활성화 트리거 명확히 정의
- [ ] README.md 업데이트

### 에이전트 추가/수정 시

- [ ] 목적과 범위 명확히 정의
- [ ] 체크리스트 항목이 실행 가능
- [ ] 리포트 포맷 템플릿 포함
- [ ] 심각도 레벨 문서화
- [ ] README.md 업데이트

## 버전 관리

plugin.json 버전 업데이트 기준:

| 변경 유형 | 버전 | 예시 |
|----------|------|------|
| 새 스킬/에이전트 추가 | minor | 1.0.0 → 1.1.0 |
| 버그 수정/개선 | patch | 1.0.0 → 1.0.1 |
| Breaking changes | major | 1.0.0 → 2.0.0 |

## 프로젝트 관리 Commands

| 커맨드 | 설명 |
|--------|------|
| `/add-skill <name>` | 새 스킬 추가 |
| `/add-agent <name>` | 새 에이전트 추가 |
| `/validate-structure` | 구조 검증 |
| `/generate-readme` | README 자동 생성 |

## 콘텐츠 스타일

- **언어**: 한국어 (코드 주석 포함)
- **코드**: TypeScript/React
- **철학**: 실용적, 과도한 추상화 지양
- **예제**: 실제 사용 가능한 코드

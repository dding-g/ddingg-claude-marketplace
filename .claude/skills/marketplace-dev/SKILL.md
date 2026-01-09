# Marketplace Development Skill

> 이 마켓플레이스 프로젝트를 개발/유지보수하기 위한 스킬

## Overview

ddingg-marketplace의 플러그인, 스킬, 에이전트를 생성, 수정, 관리하는 방법에 대한 지식을 제공합니다.

## Activation

다음 상황에서 활성화됩니다:
- plugins/ 디렉토리 파일 작업 시
- 새 플러그인, 스킬, 에이전트 생성 요청 시
- 마켓플레이스 구조 수정 시
- marketplace.json 또는 plugin.json 변경 시

## 마켓플레이스 구조

```
ddingg-claude-marketplace/
│
├── .claude-plugin/
│   └── marketplace.json              # 마켓플레이스 카탈로그
│
├── plugins/                          # 플러그인 디렉토리
│   └── frontend-claude-settings/     # 프론트엔드 플러그인
│       ├── .claude-plugin/
│       │   └── plugin.json           # 플러그인 매니페스트
│       ├── skills/                   # 배포용 스킬
│       │   ├── common/               # 공통 스킬
│       │   │   ├── writing-good-code/
│       │   │   ├── typescript-patterns/
│       │   │   ├── react-patterns/
│       │   │   ├── fsd-architecture/
│       │   │   ├── react-query-patterns/
│       │   │   └── zod-validation/
│       │   ├── nextjs-app-router/    # 플랫폼 스킬
│       │   ├── vite-csr/
│       │   └── react-native/
│       ├── agents/                   # PR 에이전트
│       │   ├── pr-review.md
│       │   ├── pr-summary.md
│       │   ├── pr-test-check.md
│       │   ├── pr-security.md
│       │   └── pr-architecture.md
│       ├── commands/                 # 배포용 명령어
│       │   └── commit.md
│       └── hooks/
│           └── hooks.json            # 플러그인 훅
│
├── .claude/                          # 로컬 개발용 (배포 안됨)
│   ├── settings.local.json
│   ├── commands/                     # 마켓플레이스 관리 명령어
│   │   ├── add-skill.md
│   │   ├── add-agent.md
│   │   ├── add-plugin.md
│   │   ├── validate-structure.md
│   │   └── generate-readme.md
│   └── skills/
│       └── marketplace-dev/          # 이 스킬
│
├── README.md
└── CONTRIBUTING.md
```

## marketplace.json 구조

```json
{
  "name": "ddingg-marketplace",
  "owner": {
    "name": "ddingg"
  },
  "metadata": {
    "description": "마켓플레이스 설명",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "플러그인 설명",
      "version": "1.0.0",
      "category": "development",
      "keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

## plugin.json 구조

각 플러그인의 `.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "author": {
    "name": "ddingg"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "development"
}
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
plugins/<plugin-name>/agents/pr-<name>.md
```

### 필수 섹션

```markdown
# PR <Name> Agent

> 에이전트 설명

## 개요
## 활성화 조건
## 체크리스트
```

## 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 마켓플레이스 | kebab-case | `ddingg-marketplace` |
| 플러그인 | kebab-case | `frontend-claude-settings` |
| 스킬 디렉토리 | kebab-case | `react-patterns` |
| 스킬 파일 | SKILL.md (대문자) | `SKILL.md` |
| 에이전트 파일 | pr-<name>.md | `pr-review.md` |
| 패턴 파일 | kebab-case.md | `data-fetching.md` |

## 프로젝트 관리 Commands

| 커맨드 | 설명 |
|--------|------|
| `/add-plugin <name>` | 새 플러그인 추가 |
| `/add-skill <name>` | 플러그인에 새 스킬 추가 |
| `/add-agent <name>` | 플러그인에 새 에이전트 추가 |
| `/validate-structure` | 마켓플레이스 구조 검증 |
| `/generate-readme` | README 자동 생성 |

## 버전 관리

| 변경 유형 | 버전 변경 | 예시 |
|----------|----------|------|
| 새 플러그인 추가 | marketplace minor | 1.0.0 → 1.1.0 |
| 플러그인 내 새 스킬/에이전트 | plugin minor | 1.0.0 → 1.1.0 |
| 버그 수정/개선 | patch | 1.0.0 → 1.0.1 |
| Breaking changes | major | 1.0.0 → 2.0.0 |

## 품질 체크리스트

### 플러그인 추가 시
- [ ] plugins/<name>/ 디렉토리 생성
- [ ] .claude-plugin/plugin.json 생성
- [ ] marketplace.json에 플러그인 등록
- [ ] README.md 업데이트

### 스킬 추가 시
- [ ] SKILL.md에 필수 섹션 포함
- [ ] 코드 예제가 문법적으로 올바름
- [ ] 좋은/나쁜 예제 모두 포함
- [ ] plugin.json 버전 업데이트

### 에이전트 추가 시
- [ ] 목적과 범위 명확히 정의
- [ ] 체크리스트 항목이 실행 가능
- [ ] plugin.json 버전 업데이트

## 콘텐츠 스타일

- **언어**: 한국어 (코드 주석 포함)
- **코드**: TypeScript/React
- **철학**: 실용적, 과도한 추상화 지양
- **예제**: 실제 사용 가능한 코드

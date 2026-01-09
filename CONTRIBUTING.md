# Contributing to ddingg-marketplace

ddingg-marketplace에 기여해 주셔서 감사합니다.

## 시작하기

### 프로젝트 클론

```bash
git clone https://github.com/dding-g/ddingg-claude-marketplace.git
cd ddingg-claude-marketplace
```

### 로컬 테스트

```bash
# 로컬 마켓플레이스 추가
/plugin marketplace add ./

# 플러그인 설치 테스트
/plugin install frontend-claude-settings@ddingg-marketplace
```

## 마켓플레이스 구조

```
ddingg-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json              # 마켓플레이스 카탈로그
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json           # 플러그인 매니페스트
│       ├── skills/                   # 스킬
│       ├── agents/                   # 에이전트
│       ├── commands/                 # 명령어
│       └── hooks/                    # 훅
└── .claude/                          # 마켓플레이스 개발용 (배포 안됨)
```

## 새 플러그인 추가하기

### 1. 디렉토리 생성

```bash
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
├── agents/
├── commands/
└── hooks/
```

또는 `/add-plugin <plugin-name>` 명령어 사용

### 2. plugin.json 작성

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "author": {
    "name": "ddingg"
  },
  "keywords": ["keyword1", "keyword2"],
  "category": "development"
}
```

### 3. marketplace.json 업데이트

```json
{
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./plugins/<plugin-name>",
      "description": "플러그인 설명",
      "version": "1.0.0"
    }
  ]
}
```

## 새 스킬 추가하기

### 1. 디렉토리 생성

```bash
# Common 스킬 (프레임워크 독립적)
plugins/<plugin-name>/skills/common/<skill-name>/SKILL.md

# Platform 스킬 (프레임워크 특화)
plugins/<plugin-name>/skills/<platform-name>/SKILL.md
plugins/<plugin-name>/skills/<platform-name>/patterns/
```

또는 `/add-skill <skill-name>` 명령어 사용

### 2. SKILL.md 구조

```markdown
# Skill Name

> 한 줄 설명

## Overview

스킬의 목적과 범위를 설명합니다.

## Activation

이 스킬은 다음 상황에서 활성화됩니다:
- 트리거 키워드 1
- 트리거 키워드 2

## Core Patterns

### 1. 패턴 이름

\`\`\`typescript
// ❌ Bad
const d = getData();

// ✅ Good
const userData = getUserData();
\`\`\`

## Best Practices

- 권장 사항 1
- 권장 사항 2

## Anti-Patterns

### ❌ 피해야 할 패턴

\`\`\`typescript
// 나쁜 예제
\`\`\`

### ✅ 대신 사용할 패턴

\`\`\`typescript
// 좋은 예제
\`\`\`
```

### 3. 코드 예제 가이드라인

- TypeScript 사용
- `✅`/`❌` 패턴으로 좋은/나쁜 예제 표시
- 실용적이고 실제 사용 가능한 코드
- 과도한 추상화 피하기
- 한국어 주석 사용

## 새 에이전트 추가하기

### 1. 파일 생성

```bash
plugins/<plugin-name>/agents/pr-<name>.md
```

또는 `/add-agent <agent-name>` 명령어 사용

### 2. 에이전트 구조

```markdown
# PR <Name> Agent

> 에이전트 설명

## 개요

에이전트의 목적과 역할을 설명합니다.

## 활성화 조건

- PR이 생성되거나 업데이트될 때
- `/<command>` 커맨드가 실행될 때

## 체크리스트

### 1. 카테고리 1

- [ ] 체크 항목 1
- [ ] 체크 항목 2

### 2. 카테고리 2

- [ ] 체크 항목 1
- [ ] 체크 항목 2

## 리포트 포맷

\`\`\`markdown
## 📋 리포트 제목

**분석 결과**: [요약]

## ✅ 통과 항목
- [통과한 항목들]

## ⚠️ 개선 필요
- [ ] [파일명:라인] 개선 내용
\`\`\`

## 심각도 레벨

| 레벨 | 설명 | 조치 |
|------|------|------|
| 🔴 Critical | 심각한 문제 | 반드시 수정 |
| 🟠 Major | 주요 문제 | 수정 권장 |
| 🟡 Minor | 사소한 문제 | 선택적 수정 |
| 🟢 Info | 참고 사항 | 정보 제공 |
```

## 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 플러그인 | kebab-case | `frontend-claude-settings` |
| 스킬 디렉토리 | kebab-case | `react-patterns` |
| 스킬 파일 | SKILL.md | `SKILL.md` |
| 에이전트 파일 | pr-<name>.md | `pr-review.md` |
| 패턴 파일 | kebab-case.md | `data-fetching.md` |

## PR 가이드라인

### 커밋 메시지

```
feat: add <skill-name> skill
fix: correct example in <skill-name>
docs: update README with new plugins
```

### PR 체크리스트

- [ ] plugin.json에 필수 필드 포함 (name, version, description)
- [ ] SKILL.md에 필수 섹션 포함 (Overview, Activation, Core Patterns)
- [ ] 코드 예제가 문법적으로 올바름
- [ ] 좋은/나쁜 예제 모두 포함
- [ ] marketplace.json 업데이트됨 (새 플러그인인 경우)
- [ ] `/validate-structure` 통과

### 한 PR에 하나의 변경

- 새 플러그인 추가: 하나의 플러그인만
- 새 스킬 추가: 하나의 스킬만
- 새 에이전트 추가: 하나의 에이전트만
- 버그 수정: 관련된 수정만

## 버전 관리

| 변경 유형 | 버전 변경 |
|----------|----------|
| 새 플러그인 | marketplace minor (1.0.0 → 1.1.0) |
| 플러그인 내 새 스킬/에이전트 | plugin minor (1.0.0 → 1.1.0) |
| 버그 수정 | patch (1.0.0 → 1.0.1) |
| Breaking changes | major (1.0.0 → 2.0.0) |

## 질문이 있으신가요?

이슈를 생성하거나 PR에 코멘트를 남겨주세요.

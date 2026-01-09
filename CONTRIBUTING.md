# Contributing to Frontend Claude Settings

프론트엔드 Claude 스킬 마켓플레이스에 기여해 주셔서 감사합니다.

## 시작하기

### 프로젝트 클론

```bash
git clone https://github.com/ddingg/ddingg-claude-marketplace.git
cd ddingg-claude-marketplace
```

### 프로젝트 관리 Commands

```bash
/add-skill <skill-name>      # 새 스킬 추가
/add-agent <agent-name>      # 새 에이전트 추가
/validate-structure          # 구조 검증
/generate-readme             # README 자동 생성
```

## 새 스킬 추가하기

### 1. 디렉토리 생성

```bash
# Common 스킬 (프레임워크 독립적)
skills/common/<skill-name>/SKILL.md

# Platform 스킬 (프레임워크 특화)
skills/<platform-name>/SKILL.md
skills/<platform-name>/patterns/<pattern-name>.md
```

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
agents/pr-<name>.md
```

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
| 디렉토리 | kebab-case | `react-patterns` |
| 스킬 파일 | SKILL.md | `SKILL.md` |
| 에이전트 파일 | pr-<name>.md | `pr-review.md` |
| 패턴 파일 | kebab-case.md | `data-fetching.md` |

## PR 가이드라인

### 커밋 메시지

```
feat: add <skill-name> skill
fix: correct example in <skill-name>
docs: update README with new commands
```

### PR 체크리스트

- [ ] SKILL.md에 필수 섹션 포함 (Overview, Activation, Core Patterns)
- [ ] 코드 예제가 문법적으로 올바름
- [ ] 좋은/나쁜 예제 모두 포함
- [ ] README.md 업데이트됨
- [ ] `/validate-structure` 통과

### 한 PR에 하나의 변경

- 새 스킬 추가: 하나의 스킬만
- 새 에이전트 추가: 하나의 에이전트만
- 버그 수정: 관련된 수정만

## 버전 관리

plugin.json 버전 업데이트:

| 변경 유형 | 버전 변경 |
|----------|----------|
| 새 스킬/에이전트 | minor (1.0.0 → 1.1.0) |
| 버그 수정 | patch (1.0.0 → 1.0.1) |
| Breaking changes | major (1.0.0 → 2.0.0) |

## 질문이 있으신가요?

이슈를 생성하거나 PR에 코멘트를 남겨주세요.

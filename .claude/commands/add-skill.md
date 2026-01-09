# Add Skill Command

> 마켓플레이스 플러그인에 새 스킬을 추가합니다

## 사용법

```
/add-skill <skill-name>
```

$ARGUMENTS 로 스킬 이름이 전달됩니다.

## 워크플로우

### 1. 플러그인 선택

사용자에게 질문:
- 어떤 플러그인에 스킬을 추가할지 선택 (기본: frontend-claude-settings)

### 2. 카테고리 확인

사용자에게 질문:
- **common**: 프레임워크 독립적인 공통 스킬
- **platform**: 특정 플랫폼 스킬 (nextjs-app-router, vite-csr, react-native)

### 3. 디렉토리 생성

카테고리에 따라 생성:

```bash
# Common 스킬
plugins/<plugin-name>/skills/common/<skill-name>/SKILL.md

# Platform 스킬
plugins/<plugin-name>/skills/<platform>/<skill-name>/SKILL.md
plugins/<plugin-name>/skills/<platform>/<skill-name>/patterns/  # 선택사항
```

### 3. SKILL.md 템플릿 생성

```markdown
# <Skill Name>

> 한 줄 설명

## Overview

스킬의 목적과 범위를 설명합니다.

## Activation

이 스킬은 다음 상황에서 활성화됩니다:
- [트리거 키워드 1]
- [트리거 키워드 2]

## Core Patterns

### 1. 패턴 이름

```typescript
// ❌ Bad
// 나쁜 예제

// ✅ Good
// 좋은 예제
```

### 2. 패턴 이름

```typescript
// 코드 예제
```

## Best Practices

- 권장 사항 1
- 권장 사항 2

## Anti-Patterns

### ❌ 피해야 할 패턴

```typescript
// 나쁜 코드
```

### ✅ 대신 사용할 패턴

```typescript
// 좋은 코드
```
```

### 4. README.md 업데이트 안내

스킬 추가 후 README.md의 스킬 테이블을 업데이트해야 합니다.

## 네이밍 컨벤션

- 디렉토리명: `kebab-case`
- 파일명: `SKILL.md` (대문자)
- 한국어 설명 사용

## 예시

```
/add-skill state-management
```

결과:
```
plugins/frontend-claude-settings/skills/common/state-management/SKILL.md
```

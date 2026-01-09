# Validate Structure Command

> 마켓플레이스 구조와 콘텐츠 품질을 검증합니다

## 사용법

```
/validate-structure
```

## 검증 항목

### 1. 디렉토리 구조 검증

```
✓ .claude-plugin/plugin.json 존재
✓ skills/ 디렉토리 존재
✓ agents/ 디렉토리 존재
```

각 스킬 디렉토리 확인:
- [ ] SKILL.md 파일 존재
- [ ] kebab-case 네이밍
- [ ] 빈 디렉토리 없음

### 2. SKILL.md 필수 섹션 검증

각 SKILL.md 파일에 다음 섹션이 있는지 확인:

```markdown
# 제목 (필수)
> 한 줄 설명 (필수)

## Overview 또는 개요 (필수)
## Activation 또는 활성화 (필수)
## Core Patterns 또는 핵심 패턴 (필수)
## Best Practices 또는 권장 사항 (선택)
## Anti-Patterns 또는 안티패턴 (선택)
```

### 3. 에이전트 파일 검증

각 에이전트 파일에 다음 섹션이 있는지 확인:

```markdown
# PR <Name> Agent (필수)
## 개요 (필수)
## 활성화 조건 (필수)
## 체크리스트 (필수)
## 리포트 포맷 (선택)
## 심각도 레벨 (선택)
```

### 4. plugin.json 검증

필수 필드 확인:
- [ ] name
- [ ] version (semver 형식)
- [ ] description

### 5. README 동기화 검증

- [ ] 모든 스킬이 README에 나열됨
- [ ] 모든 에이전트가 README에 나열됨
- [ ] 커맨드 문서화됨

## 출력 형식

```markdown
## 📋 구조 검증 결과

### ✅ 통과 (N개)
- skills/common/writing-good-code/SKILL.md
- skills/common/typescript-patterns/SKILL.md
...

### ⚠️ 경고 (N개)
- skills/nextjs-app-router/SKILL.md: Best Practices 섹션 없음
...

### ❌ 오류 (N개)
- skills/new-skill/: SKILL.md 파일 없음
...

### 📊 요약
- 스킬: 10개 검증됨
- 에이전트: 5개 검증됨
- 통과율: 95%
```

## 검증 명령어 (참고용)

실제 검증 시 사용할 수 있는 명령어:

```bash
# 모든 SKILL.md 파일 찾기
find skills -name "SKILL.md"

# 모든 에이전트 파일 찾기
find agents -name "*.md"

# plugin.json 확인
cat .claude-plugin/plugin.json
```

## 자동 수정 제안

오류 발견 시 수정 제안:
- SKILL.md 없음 → 템플릿 생성 제안
- 필수 섹션 없음 → 섹션 추가 제안
- README 미동기화 → README 업데이트 제안

# Validate Structure Command

> 마켓플레이스 구조와 콘텐츠 품질을 검증합니다

## 사용법

```
/validate-structure
```

## 검증 항목

### 1. 마켓플레이스 구조 검증

```
✓ .claude-plugin/marketplace.json 존재
✓ plugins/ 디렉토리 존재
```

marketplace.json 필수 필드:
- [ ] name (마켓플레이스 이름)
- [ ] owner.name (소유자)
- [ ] plugins (플러그인 목록)

### 2. 플러그인 구조 검증

각 플러그인 디렉토리 확인:

```
plugins/<plugin-name>/
├── .claude-plugin/plugin.json  ← 필수
├── skills/                     ← 선택
├── agents/                     ← 선택
├── commands/                   ← 선택
└── hooks/                      ← 선택
```

plugin.json 필수 필드:
- [ ] name
- [ ] version (semver 형식)
- [ ] description

### 3. SKILL.md 필수 섹션 검증

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

### 4. 에이전트 파일 검증

각 에이전트 파일에 다음 섹션이 있는지 확인:

```markdown
# PR <Name> Agent (필수)
## 개요 (필수)
## 활성화 조건 (필수)
## 체크리스트 (필수)
## 리포트 포맷 (선택)
## 심각도 레벨 (선택)
```

### 5. marketplace.json과 플러그인 동기화 검증

- [ ] plugins/ 내 모든 플러그인이 marketplace.json에 나열됨
- [ ] marketplace.json의 source 경로가 유효함
- [ ] 버전 정보가 일치함

### 6. README 동기화 검증

- [ ] 모든 플러그인이 README에 나열됨
- [ ] 설치 방법이 문서화됨

## 출력 형식

```markdown
## 📋 마켓플레이스 구조 검증 결과

### 마켓플레이스
- ✅ marketplace.json 유효
- ✅ 플러그인 1개 등록됨

### 플러그인: frontend-claude-settings
- ✅ plugin.json 유효
- ✅ skills/: 9개 스킬
- ✅ agents/: 5개 에이전트
- ✅ commands/: 1개 명령어
- ✅ hooks/: hooks.json 유효

### ⚠️ 경고 (N개)
- plugins/frontend-claude-settings/skills/...: Best Practices 섹션 없음

### ❌ 오류 (N개)
- plugins/new-plugin/: plugin.json 없음

### 📊 요약
- 플러그인: 1개
- 스킬: 9개
- 에이전트: 5개
- 통과율: 100%
```

## 검증 명령어 (참고용)

실제 검증 시 사용할 수 있는 명령어:

```bash
# marketplace.json 확인
cat .claude-plugin/marketplace.json

# 모든 플러그인의 plugin.json 찾기
find plugins -name "plugin.json"

# 모든 SKILL.md 파일 찾기
find plugins -name "SKILL.md"

# 모든 에이전트 파일 찾기
find plugins -path "*/agents/*.md"

# Claude Code 공식 검증
claude plugin validate .
```

## 자동 수정 제안

오류 발견 시 수정 제안:
- marketplace.json 없음 → 생성 제안
- plugin.json 없음 → 템플릿 생성 제안
- SKILL.md 없음 → 템플릿 생성 제안
- 필수 섹션 없음 → 섹션 추가 제안
- 동기화 오류 → marketplace.json 업데이트 제안

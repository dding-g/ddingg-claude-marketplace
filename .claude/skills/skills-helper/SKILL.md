# Claude Code Skills 작성 가이드

## 개요

이 문서는 Claude Code가 고품질 Skills를 작성할 수 있도록 하는 가이드입니다. Skills는 Claude의 기능을 확장하는 모듈식 패키지로, 특정 도메인의 전문 지식, 워크플로우, 도구 통합을 제공합니다.

---

## Skills의 본질

Skills는 Claude에게 **"온보딩 가이드"** 역할을 합니다. 핵심 질문: "범용 에이전트를 전문 에이전트로 변환하기 위해 어떤 절차적 지식이 필요한가?"

### Skills가 제공하는 것

| 구성요소 | 설명 | 예시 |
|---------|------|------|
| **전문 워크플로우** | 특정 도메인의 다단계 절차 | PDF 폼 작성 5단계 프로세스 |
| **도구 통합** | 특정 파일 포맷/API 작업 지침 | docx XML 편집, AWS API 호출 |
| **도메인 전문성** | 회사 고유 지식, 스키마, 비즈니스 로직 | DB 스키마, 사내 정책 |
| **번들 리소스** | 반복 작업용 스크립트, 참조 문서, 에셋 | Python 유틸리티, 템플릿 파일 |

---

## 핵심 원칙

### 1. 간결함이 핵심 (Context Window는 공유 자원)

```
❌ 피해야 할 것
"Docker는 컨테이너화 플랫폼으로..."와 같은 일반적 설명

✅ 해야 할 것
"docker build -t myapp . && docker run -p 3000:3000 myapp" 같은 실행 가능한 예제
```

**검증 질문:**
- "Claude가 이 설명 없이도 이미 알고 있는가?"
- "이 단락이 토큰 비용을 정당화하는가?"

### 2. 적절한 자유도 설정

| 자유도 | 사용 시점 | 형식 |
|--------|----------|------|
| **높음** | 여러 접근법이 유효할 때 | 텍스트 기반 지침 |
| **중간** | 선호하는 패턴이 있지만 변형 가능할 때 | 의사코드/파라미터화된 스크립트 |
| **낮음** | 연산이 취약하고 일관성이 중요할 때 | 구체적 스크립트, 적은 파라미터 |

**비유:** Claude가 길을 탐색한다고 생각하라. 절벽 옆 좁은 다리는 구체적 가이드레일(낮은 자유도)이 필요하고, 열린 들판은 여러 경로 허용(높은 자유도).

### 3. Progressive Disclosure (점진적 공개)

```
Level 1: 메타데이터 (항상 컨텍스트에 로드) - ~100단어
  └── name + description만

Level 2: SKILL.md 본문 (스킬 트리거 시 로드) - <5,000단어
  └── 핵심 지침과 워크플로우

Level 3: 번들 리소스 (필요 시 로드) - 무제한
  └── scripts/, references/, assets/
```

---

## 디렉토리 구조

```
skill-name/
├── SKILL.md              # 필수: 메타데이터 + 지침
├── scripts/              # 선택: 실행 가능한 코드
│   └── rotate_pdf.py
├── references/           # 선택: 참조 문서
│   └── api_docs.md
└── assets/               # 선택: 출력물에 사용되는 파일
    └── template.pptx
```

### 각 디렉토리의 역할

#### `scripts/` - 결정적 실행이 필요한 코드

```python
# scripts/extract_text.py
# 언제 포함: 동일 코드가 반복 재작성될 때
# 장점: 토큰 효율적, 결정적, 컨텍스트 로드 없이 실행 가능
```

#### `references/` - 컨텍스트에 로드되는 참조 문서

```markdown
# references/schema.md
# 언제 포함: Claude가 작업 중 참조해야 할 문서
# 예시: DB 스키마, API 문서, 회사 정책
# 팁: 10k 단어 초과 시 SKILL.md에 grep 패턴 포함
```

#### `assets/` - 출력물에 사용되는 파일

```
# assets/logo.png, assets/template.pptx
# 언제 포함: 최종 출력물에 사용될 파일
# 예시: 브랜드 에셋, 템플릿, 보일러플레이트 코드
```

---

## SKILL.md 작성법

### Frontmatter (YAML) - 필수

```yaml
---
name: skill-name
description: |
  [스킬이 하는 것] + [트리거 조건/사용 시점]
  구체적 예: "Comprehensive document creation, editing, and analysis 
  with support for tracked changes, comments, formatting preservation.
  When Claude needs to work with professional documents (.docx files) for:
  (1) Creating new documents, (2) Modifying or editing content, 
  (3) Working with tracked changes, (4) Adding comments"
---
```

**description 작성 체크리스트:**
- [ ] 스킬이 무엇을 하는지 명확히 설명
- [ ] 트리거 조건 포함 (언제 이 스킬을 사용해야 하는가?)
- [ ] "When to Use" 섹션은 본문이 아닌 description에 포함
- [ ] 구체적 키워드 포함 (파일 확장자, 기술 스택 등)

### Body (Markdown) - 지침

```markdown
# 스킬 이름

## Overview
[한 문단으로 핵심 요약]

## Quick Reference
[가장 많이 사용되는 패턴 - 표 형식 추천]

| Task | Approach |
|------|----------|
| 읽기/분석 | `command` 또는 script |
| 생성 | See Creating below |
| 편집 | See Editing below |

## Creating [대상]
[구체적 코드 예제와 함께]

## Editing [대상]
[구체적 코드 예제와 함께]

## Critical Rules
[반드시 지켜야 할 규칙 - 불릿 리스트]

## Dependencies
[필요한 패키지/도구]
```

---

## 패턴별 가이드

### Pattern 1: Sequential Workflow (순차 워크플로우)

```markdown
## Process

PDF 폼 작성은 다음 단계를 따른다:

1. 폼 분석 (`scripts/analyze_form.py` 실행)
2. 필드 매핑 생성 (fields.json 편집)
3. 매핑 검증 (`scripts/validate_fields.py` 실행)
4. 폼 작성 (`scripts/fill_form.py` 실행)
5. 출력 검증 (`scripts/verify_output.py` 실행)
```

### Pattern 2: Conditional Workflow (조건부 워크플로우)

```markdown
## Workflow Selection

1. 작업 유형 판단:
   - **새 콘텐츠 생성?** → "Creation Workflow" 따르기
   - **기존 콘텐츠 편집?** → "Editing Workflow" 따르기

## Creation Workflow
[생성 단계]

## Editing Workflow
[편집 단계]
```

### Pattern 3: Domain-Specific Organization (도메인별 조직화)

```
bigquery-skill/
├── SKILL.md              # 개요와 네비게이션
└── references/
    ├── finance.md        # 매출, 청구 메트릭
    ├── sales.md          # 기회, 파이프라인
    └── product.md        # API 사용량, 기능
```

SKILL.md에서:
```markdown
## Domain References

- **Finance queries**: See [finance.md](references/finance.md)
- **Sales queries**: See [sales.md](references/sales.md)
- **Product queries**: See [references/product.md](references/product.md)
```

### Pattern 4: Template Pattern (템플릿 패턴)

```markdown
## Output Format

### Strict (API 응답, 데이터 포맷)
ALWAYS use this exact structure:
[정확한 템플릿]

### Flexible (적응이 유용한 경우)
Here is a sensible default, adapt as needed:
[기본 템플릿]
```

### Pattern 5: Examples Pattern (예제 패턴)

```markdown
## Commit Message Format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
```
fix(reports): correct date formatting in timezone conversion
```
```

---

## Critical Rules (절대 규칙)

### ❌ 포함하지 말 것

```
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- 사용자 대상 문서
- 스킬 생성 과정에 대한 메타 정보
```

### ✅ 반드시 지킬 것

1. **SKILL.md는 500줄 미만 유지**
   - 초과 시 references/로 분리

2. **참조 파일은 1단계 깊이만**
   - SKILL.md → references/file.md ✅
   - SKILL.md → references/a.md → references/b.md ❌

3. **100줄 초과 참조 파일은 목차 포함**
   ```markdown
   # API Reference

   ## Table of Contents
   - [Authentication](#authentication)
   - [Endpoints](#endpoints)
   - [Error Codes](#error-codes)
   ```

4. **정보 중복 금지**
   - SKILL.md 또는 references 중 한 곳에만 정보 배치

5. **명령형/부정사 형태 사용**
   - "Use pandoc to extract text" ✅
   - "Pandoc can be used to extract text" ❌

---

## 스킬 생성 프로세스

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Understanding                                           │
│  • 구체적 사용 예시 수집                                          │
│  • "어떤 기능을 지원해야 하는가?"                                  │
│  • "사용자가 어떻게 이 스킬을 트리거할까?"                         │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Planning                                                │
│  • 각 예시에 대해 처음부터 실행 방법 분석                          │
│  • 반복적으로 필요한 scripts, references, assets 식별             │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: Initialize                                              │
│  • scripts/init_skill.py <skill-name> --path <output-dir>       │
│  • 템플릿 디렉토리 생성됨                                         │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: Edit                                                    │
│  • scripts/, references/, assets/ 구현                           │
│  • SKILL.md frontmatter + body 작성                              │
│  • 스크립트는 실제 실행하여 테스트                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: Package                                                 │
│  • scripts/package_skill.py <path/to/skill-folder>              │
│  • 자동 검증 + .skill 파일 생성                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 6: Iterate                                                 │
│  • 실제 작업에 스킬 사용                                          │
│  • 비효율 발견 → 개선 → 재테스트                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 실전 예제: DOCX Skill 분석

### Frontmatter 분석

```yaml
---
name: docx
description: "Comprehensive document creation, editing, and analysis 
  with support for tracked changes, comments, formatting preservation, 
  and text extraction. When Claude needs to work with professional 
  documents (.docx files) for: (1) Creating new documents, 
  (2) Modifying or editing content, (3) Working with tracked changes, 
  (4) Adding comments, or any other document tasks"
---
```

**좋은 점:**
- 구체적 기능 나열 (tracked changes, comments, formatting)
- 명확한 트리거 조건 (1~4 번호로 구분)
- 파일 확장자 명시 (.docx)

### Body 구조 분석

```markdown
# DOCX creation, editing, and analysis

## Overview
[한 문장 요약]

## Quick Reference
[표 형식 - 작업별 접근법]

## Creating New Documents
[docx-js 사용법 + 상세 코드]

## Editing Existing Documents
[3단계 프로세스: Unpack → Edit → Pack]

## XML Reference
[편집 시 필요한 XML 패턴]

## Critical Rules for docx-js
[절대 규칙 목록]

## Dependencies
[필요 패키지]
```

**구조적 특징:**
- Quick Reference로 빠른 탐색 지원
- Creating/Editing 분리 (조건부 워크플로우)
- Critical Rules로 실수 방지
- 코드 예제에 ❌ WRONG / ✅ CORRECT 대비

---

## Quality Checklist

스킬 완성 전 다음을 확인:

### Frontmatter
- [ ] `name`과 `description` 필드 존재
- [ ] `description`에 트리거 조건 포함
- [ ] 불필요한 필드 없음

### SKILL.md Body
- [ ] 500줄 미만
- [ ] Quick Reference 또는 개요 섹션 존재
- [ ] 코드 예제 포함
- [ ] Critical Rules/Common Pitfalls 섹션 존재
- [ ] 참조 파일 경로 정확

### Resources
- [ ] scripts/ - 모든 스크립트 실행 테스트 완료
- [ ] references/ - SKILL.md에서 참조됨
- [ ] assets/ - 필요한 템플릿/에셋만 포함
- [ ] 불필요한 예제 파일 삭제됨

### 구조
- [ ] 정보 중복 없음
- [ ] 참조 파일 1단계 깊이
- [ ] 긴 참조 파일에 목차 포함

---

## Anti-Patterns (피해야 할 것)

### 1. 과도한 일반 설명

```markdown
❌ Bad:
"Docker is a platform for developing, shipping, and running 
applications in containers. Containers are lightweight..."

✅ Good:
## Docker Commands
docker build -t myapp . && docker run -p 3000:3000 myapp
```

### 2. 트리거 조건 본문 배치

```markdown
❌ Bad (본문에 "When to Use"):
## When to Use This Skill
Use this skill when you need to...

✅ Good (description에 배치):
description: "... Use when Claude needs to work with .docx files for..."
```

### 3. 깊은 참조 중첩

```markdown
❌ Bad:
SKILL.md → references/a.md → references/b.md → references/c.md

✅ Good:
SKILL.md → references/a.md
SKILL.md → references/b.md
SKILL.md → references/c.md
```

### 4. 중복 정보

```markdown
❌ Bad:
SKILL.md에 "API는 JSON 반환..."
references/api.md에도 "API는 JSON 반환..."

✅ Good:
SKILL.md: "API 상세는 references/api.md 참조"
references/api.md: "API는 JSON 반환..."
```

---

## 요약

| 원칙 | 핵심 |
|------|------|
| **간결함** | Claude가 이미 아는 것 제외, 토큰 비용 정당화 |
| **자유도** | 작업 fragility에 맞게 specificity 조절 |
| **Progressive Disclosure** | 메타데이터 → SKILL.md → resources 단계적 로딩 |
| **구조** | SKILL.md + scripts/ + references/ + assets/ |
| **품질** | 테스트, 불필요 파일 제거, Critical Rules 포함 |

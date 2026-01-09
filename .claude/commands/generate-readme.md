# Generate README Command

> skills와 agents로부터 README.md를 자동 생성합니다

## 사용법

```
/generate-readme
```

## 워크플로우

### 1. 스킬 스캔

`skills/` 디렉토리를 스캔하여 메타데이터 추출:

```bash
skills/
├── common/           # 공통 스킬
│   ├── writing-good-code/
│   ├── typescript-patterns/
│   └── ...
├── nextjs-app-router/  # 플랫폼 스킬
├── vite-csr/
└── react-native/
```

각 SKILL.md에서 추출:
- 제목 (첫 번째 `#` 헤더)
- 설명 (`>` 인용문)
- 활성화 키워드 (Activation 섹션)

### 2. 에이전트 스캔

`agents/` 디렉토리를 스캔:

```bash
agents/
├── pr-review.md
├── pr-summary.md
├── pr-test-check.md
├── pr-security.md
└── pr-architecture.md
```

각 에이전트에서 추출:
- 제목
- 설명
- 트리거 커맨드

### 3. README 섹션 생성

#### Common Skills 테이블

```markdown
### Common Skills

| 스킬 | 핵심 내용 |
|------|----------|
| **writing-good-code** | 이름 짓기, 함수 분리, 조건문, Early Return |
| **typescript-patterns** | 타입 추론, 유틸리티 타입, 제네릭, 타입 좁히기 |
...
```

#### Platform Skills 테이블

```markdown
### Platform Skills

| 스킬 | 대상 |
|------|------|
| **nextjs-app-router** | Server Components, Server Actions, 데이터 페칭 |
| **vite-csr** | React Router, Zustand, 코드 스플리팅 |
| **react-native** | Expo Router, 네이티브 기능, 성능 최적화 |
```

#### PR 에이전트 테이블

```markdown
## PR 에이전트

| 에이전트 | 역할 | 커맨드 |
|---------|------|--------|
| **PR Review** | 코드 품질, 보안, 성능 | `/review` |
| **PR Summary** | 변경사항 요약 | `/summary` |
...
```

### 4. README 구조

생성되는 README.md 구조:

```markdown
# Frontend Claude Settings

프론트엔드 개발을 위한 Claude 스킬 및 에이전트

## 설치

[플러그인 설치 방법]

## 📁 구조

[디렉토리 구조]

## 철학

[프로젝트 철학 - 기존 내용 유지]

## 스킬 개요

### Common Skills
[자동 생성된 테이블]

### Platform Skills
[자동 생성된 테이블]

## PR 에이전트

[자동 생성된 테이블]

## 프로젝트 관리 Commands

[프로젝트 내부 명령어]

## 사용법

[사용법]

## 컨벤션

[컨벤션 - 기존 내용 유지]
```

## 옵션

- `--dry-run`: 미리보기만 (파일 수정 없음)
- `--section=skills`: 특정 섹션만 업데이트

## 기존 내용 보존

다음 섹션은 기존 내용을 유지:
- 철학 (## 철학)
- 컨벤션 (## 컨벤션)
- 사용자 정의 섹션

## 출력 예시

```
📝 README.md 생성 완료

스캔된 항목:
- Common Skills: 6개
- Platform Skills: 4개
- PR Agents: 5개

업데이트된 섹션:
- ✅ 스킬 개요
- ✅ PR 에이전트
- ⏭️ 철학 (보존됨)
- ⏭️ 컨벤션 (보존됨)
```

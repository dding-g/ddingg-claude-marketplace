# ddingg-marketplace

프론트엔드 개발을 위한 Claude Code 플러그인 마켓플레이스

## 설치

### 마켓플레이스 추가

```bash
/plugin marketplace add dding-g/ddingg-claude-marketplace
```

### 플러그인 설치

```bash
# 공통 스킬
/plugin install common-skills@ddingg-marketplace

# 플랫폼별 스킬
/plugin install nextjs-app-router@ddingg-marketplace
/plugin install vite-csr@ddingg-marketplace
/plugin install react-native@ddingg-marketplace

# PR 에이전트
/plugin install pr-agents@ddingg-marketplace

# Maestro E2E 테스트
/plugin install react-native-test-maestro@ddingg-marketplace

# 유틸리티
/plugin install utils@ddingg-marketplace

# Slack 알림
/plugin install slack-notify@ddingg-marketplace
```

### 로컬 테스트

```bash
# 저장소 클론
git clone https://github.com/dding-g/ddingg-claude-marketplace.git

# 로컬 마켓플레이스 추가
/plugin marketplace add ./ddingg-claude-marketplace

# 플러그인 설치
/plugin install common-skills@ddingg-marketplace
```

## 📁 구조

```
ddingg-claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json              # 마켓플레이스 카탈로그
│
├── plugins/
│   ├── common-skills/                # 공통 스킬 (6개)
│   ├── nextjs-app-router/            # Next.js 15+ App Router
│   ├── vite-csr/                     # Vite CSR/SPA
│   ├── react-native/                 # React Native/Expo
│   ├── react-native-test-maestro/    # Maestro E2E 테스트
│   ├── pr-agents/                    # PR 에이전트 (5개)
│   ├── utils/                        # 유틸리티 (commit, hooks)
│   ├── codebase-onboarding/          # 코드베이스 온보딩 도구
│   ├── slack-notify/                 # Slack 알림 (commit 후 자동 알림)
│   ├── agents-md/                    # AGENTS.md 작성 패턴
│   └── react-table-patterns/         # TanStack React Table 패턴
│
└── .claude/                          # 마켓플레이스 개발용 (배포 안됨)
```

## 플러그인

### common-skills

프레임워크 독립적인 공통 프론트엔드 스킬

| 스킬 | 핵심 내용 |
|------|----------|
| **writing-good-code** | 이름 짓기, 함수 분리, 조건문, Early Return |
| **typescript-patterns** | 타입 추론, 유틸리티 타입, 제네릭, 타입 좁히기 |
| **react-patterns** | 상태 관리 판단, Suspense, React 19 패턴 |
| **fsd-architecture** | 언제 FSD를 쓸까? 실용적 적용법 |
| **react-query-patterns** | Query Factory, queryOptions/mutationOptions 패턴 |
| **zod-validation** | 폼 검증, API 응답 검증, 핵심 패턴 3가지 |

### nextjs-app-router

Next.js 15+ App Router 전용 스킬

- Server Components, Server Actions
- 데이터 페칭 패턴
- 캐싱 전략

### vite-csr

Vite + React SPA 전용 스킬

- React Router 패턴
- Zustand 상태 관리
- 코드 스플리팅

### react-native

React Native/Expo 전용 스킬

- Expo Router 패턴
- 네이티브 기능 통합
- 성능 최적화

### pr-agents

PR 코드 리뷰 에이전트

| 에이전트 | 역할 | 커맨드 |
|---------|------|--------|
| **PR Review** | 코드 품질, 보안, 성능 | `/review` |
| **PR Summary** | 변경사항 요약 | `/summary` |
| **Test Check** | 테스트 커버리지 | `/test-check` |
| **Security** | 보안 취약점 | `/security` |
| **Architecture** | FSD 아키텍처 검증 | `/arch` |

### react-native-test-maestro

React Native Maestro E2E 테스트 도구

| 커맨드/에이전트 | 역할 |
|----------------|------|
| `/maestro` | 전체 워크플로우 실행 (설정 → 플랜 → 검증 → 테스트) |
| **maestro-test-plan** | 테스트 플랜 작성 전문가 |
| **flow-validation** | 플로우 파일 검증 전문가 |
| **tester** | 테스트 실행 및 분석 전문가 |

### utils

유틸리티 명령어

| 커맨드 | 설명 |
|--------|------|
| `/commit` | Conventional commit 형식으로 커밋 및 push |
| `/commit --no-push` | 커밋만 하고 push 생략 |

### slack-notify

Slack 알림 플러그인

| 기능 | 설명 |
|------|------|
| **PostToolUse Hook** | git commit 성공 시 자동 Slack 알림 |
| `/notify-slack` | 수동으로 작업 완료 알림 전송 |

환경 변수: `SLACK_WEBHOOK_URL` 필요

### agents-md

AGENTS.md 파일 작성 패턴

- 패시브 컨텍스트 vs 스킬 비교
- 압축 인덱스 구조
- 토큰 절약 기법

### react-table-patterns

TanStack React Table 사용 패턴

- DataGrid 래퍼 컴포넌트
- 컬럼 정의 팩토리 패턴
- 행 선택, 정렬, 페이지네이션

## 철학

- **심플하게 시작, 필요할 때 확장**
- 교과서적 규칙보다 **실용적 판단**
- 과도한 추상화보다 **명확한 코드**
- 트렌드 추종보다 **문제 해결**

## 사용법

스킬은 관련 키워드 감지 시 자동 활성화됩니다.

PR 에이전트는 커맨드로 실행:
```
/review
/summary
/security
```

## 마켓플레이스 개발

이 마켓플레이스를 개발/유지보수하기 위한 로컬 명령어:

| 커맨드 | 설명 |
|--------|------|
| `/add-plugin <name>` | 새 플러그인 추가 |
| `/add-skill <name>` | 플러그인에 새 스킬 추가 |
| `/add-agent <name>` | 플러그인에 새 에이전트 추가 |
| `/validate-structure` | 마켓플레이스 구조 검증 |
| `/optimize-skills` | SKILL.md 파일 품질 분석 및 최적화 제안 |
| `/generate-readme` | README 자동 생성 |

## 컨벤션

- 파일명: `kebab-case`
- 컴포넌트: `PascalCase`
- 훅: `useCamelCase`
- 상수: `SCREAMING_SNAKE_CASE`

## 스펙 준수

모든 파일은 Claude Code 공식 플러그인 스펙을 준수합니다:

- **plugin.json**: `name`, `version`, `description`, `author`, `keywords`, `hooks` 필드만 사용 (`category` 등 미지원)
- **hooks.json**: 이벤트별 객체 구조 (`PreToolUse`, `PostToolUse` 등), `matcher`와 `hooks` 배열 사용
- **SKILL.md**: YAML frontmatter (`name`, `description`)
- **Agent files**: YAML frontmatter (`name`, `description`, `tools`)
- **Command files**: YAML frontmatter (`name`, `description`)

## 기여하기

[CONTRIBUTING.md](./CONTRIBUTING.md) 참고

---
name: maestro
description: Maestro E2E 테스트 전체 워크플로우 실행. 설정 확인, 테스트 플랜 작성, 플로우 검증, 테스트 실행을 순차적으로 수행합니다.
---

# Maestro E2E Testing

> React Native 프로젝트의 Maestro E2E 테스트 설정, 작성, 실행, 분석을 수행합니다.

## 워크플로우

이 커맨드는 다음 순서로 진행됩니다:

```
[설정 확인] → [테스트 플랜 작성] → [플로우 검증] → [테스트 실행 및 분석]
```

---

## Phase 0: Maestro 설정 확인

먼저 프로젝트의 Maestro 설정 상태를 확인합니다.

### 확인 항목

1. **Maestro CLI 설치 확인**
   ```bash
   maestro --version
   ```
   - 설치 안 됨 → 설치 안내

2. **프로젝트 구조 확인**
   - `.maestro/` 폴더 존재 여부
   - 기존 플로우 파일 존재 여부

3. **앱 설정 확인**
   - `app.json` 또는 `app.config.js`에서 appId 확인
   - iOS: `bundleIdentifier`
   - Android: `package`

### 설정이 안 되어 있는 경우

다음 설정을 순차적으로 진행합니다:

#### 1. Maestro CLI 설치
```bash
# macOS
curl -Ls "https://get.maestro.mobile.dev" | bash

# 설치 확인
maestro --version
```

#### 2. 프로젝트 초기화
```bash
# .maestro 폴더 생성
mkdir -p .maestro
```

#### 3. 기본 설정 파일 생성

**.maestro/config.yaml** (선택사항)
```yaml
# Maestro 전역 설정
flows:
  - .maestro/*.yaml
```

#### 4. 첫 번째 플로우 파일 템플릿 생성

**.maestro/app-launch.yaml**
```yaml
appId: ${APP_ID}  # 환경변수로 관리
---
- launchApp
- assertVisible:
    text: "앱의 첫 화면 텍스트"
```

#### 5. 환경 변수 설정 안내
```bash
# iOS 시뮬레이터용
export APP_ID="com.yourcompany.yourapp"

# Android 에뮬레이터용
export APP_ID="com.yourcompany.yourapp"
```

#### 6. testID 추가 가이드

React Native 컴포넌트에 testID 추가:
```tsx
// ✅ 테스트 가능한 컴포넌트
<TouchableOpacity testID="login-button">
  <Text>로그인</Text>
</TouchableOpacity>

<TextInput testID="email-input" />

// Maestro에서 사용
// - tapOn: { id: "login-button" }
// - inputText: { id: "email-input", text: "test@example.com" }
```

---

## Phase 1: 테스트 플랜 작성

**Agent: `agents/maestro-test-plan.md`**

설정이 완료되면 테스트 플랜 작성을 시작합니다.

### 수행 작업
1. 프로젝트의 화면/기능 분석
2. testID 현황 파악
3. 테스트 시나리오 설계 (Happy path, Edge cases)
4. Maestro 플로우 파일 생성

### 결과물
- 테스트 시나리오 문서
- `.maestro/*.yaml` 플로우 파일들

---

## Phase 2: 플로우 검증

**Agent: `agents/flow-validation.md`**

생성된 플로우 파일을 검증합니다.

### 수행 작업
1. YAML 문법 검증
2. Maestro 명령어 유효성 확인
3. selector 패턴 검증
4. 안정성 검사 (하드코딩된 sleep 등)
5. 베스트 프랙티스 준수 확인

### 결과물
- 검증 리포트
- 개선 필요 항목 목록

---

## Phase 3: 테스트 실행 및 분석

**Agent: `agents/tester.md`**

검증된 플로우를 실제로 실행합니다.

### 사전 조건
- iOS Simulator 또는 Android Emulator 실행 중
- 앱이 빌드되어 설치된 상태

### 수행 작업
1. Maestro 테스트 실행
2. 성공/실패 결과 수집
3. 실패 원인 분석 (앱 버그 vs 테스트 문제)
4. Flaky 테스트 식별
5. 개선사항 및 버그 리포트

### 결과물
- 테스트 실행 리포트
- 발견된 버그 목록
- 테스트/앱 개선 제안

---

## 실행 모드

사용자에게 실행 모드를 확인합니다:

1. **전체 실행**: Phase 0 → 1 → 2 → 3 순차 실행
2. **설정만**: Phase 0만 실행 (초기 설정)
3. **테스트 플랜만**: Phase 1만 실행
4. **검증만**: Phase 2만 실행
5. **테스트 실행만**: Phase 3만 실행

---

## 최종 리포트 포맷

```markdown
# Maestro E2E 테스트 리포트

## 실행 요약
- 실행 일시: [날짜/시간]
- 실행 모드: [전체/부분]
- 총 소요 시간: [시간]

## Phase 0: 설정 상태
- Maestro CLI: [버전]
- 프로젝트 설정: [완료/신규 설정]
- appId: [앱 ID]

## Phase 1: 테스트 플랜
- 분석된 화면: [N]개
- 생성된 플로우: [N]개
- testID 현황: [존재/누락] 개수

## Phase 2: 플로우 검증
- 검증된 파일: [N]개
- Critical 이슈: [N]개
- Major 이슈: [N]개
- Minor 이슈: [N]개

## Phase 3: 테스트 결과
- 통과율: [N]%
- 성공: [N]개
- 실패: [N]개
- Flaky: [N]개

## 발견된 이슈

### 앱 버그
- [ ] [버그 설명] - [심각도]

### 테스트 개선 필요
- [ ] [개선 내용]

### 권장 사항
[추가 권장 사항]
```

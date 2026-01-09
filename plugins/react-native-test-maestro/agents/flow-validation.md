# Flow Validation Agent

> Maestro 플로우 파일 검증 전문가

## 역할

`.maestro/` 폴더의 모든 플로우 파일을 검증하여 문법 오류, 구조 문제, 안정성 이슈를 사전에 발견합니다.

## 검증 항목

### 1. YAML 문법 검증

- [ ] 올바른 YAML 구문
- [ ] 들여쓰기 일관성
- [ ] 특수문자 이스케이프

```yaml
# ✅ 올바름
- assertVisible:
    text: "확인"

# ❌ 잘못됨 - 들여쓰기 오류
- assertVisible:
text: "확인"
```

### 2. Maestro 구조 검증

#### 필수 헤더
```yaml
appId: ${APP_ID}  # 또는 실제 앱 ID
---
# 플로우 명령어들
```

#### 선택적 헤더
```yaml
appId: ${APP_ID}
name: "플로우 설명"
tags:
  - smoke
  - auth
env:
  USERNAME: "test@example.com"
---
```

### 3. 명령어 유효성

#### 지원되는 명령어 목록
```yaml
# 앱 제어
- launchApp
- stopApp
- clearState
- clearKeychain

# 탭/클릭
- tapOn
- doubleTapOn
- longPressOn

# 입력
- inputText
- eraseText
- hideKeyboard

# 스크롤/스와이프
- scroll
- scrollUntilVisible
- swipe

# 대기
- waitForAnimationToEnd
- extendedWaitUntil

# 검증
- assertVisible
- assertNotVisible

# 조건부
- runFlow
- runScript

# 기타
- back
- repeat
- copyTextFrom
- pasteText
- takeScreenshot
```

#### 잘못된 명령어 검출
```yaml
# ❌ 존재하지 않는 명령어
- clickOn:  # tapOn 사용해야 함
    id: "button"

# ❌ 잘못된 파라미터
- tapOn:
    identifier: "button"  # id 사용해야 함
```

### 4. Selector 검증

#### 유효한 selector
```yaml
- tapOn:
    id: "button-id"           # testID
- tapOn:
    text: "버튼 텍스트"        # 텍스트
- tapOn:
    label: "접근성 라벨"       # accessibilityLabel
- tapOn:
    index: 0                   # 인덱스 (비권장)
```

#### Selector 패턴 검사
```yaml
# ⚠️ 경고 - 불안정한 패턴
- tapOn:
    index: 0  # 순서 변경 시 실패

# ⚠️ 경고 - 동적 텍스트
- tapOn:
    text: "2024년 1월 15일"  # 날짜는 변경됨

# ✅ 권장 - 안정적인 testID
- tapOn:
    id: "date-picker-button"
```

### 5. 안정성 검증

#### 하드코딩된 대기 시간
```yaml
# ❌ 피해야 함
- swipe:
    direction: DOWN
- sleep: 2000  # 하드코딩된 대기

# ✅ 권장
- swipe:
    direction: DOWN
- waitForAnimationToEnd
```

#### 타임아웃 설정
```yaml
# ✅ 명시적 타임아웃
- assertVisible:
    id: "loading-complete"
    timeout: 10000  # 10초
```

#### 재시도 로직
```yaml
# ✅ 불안정한 동작에 재시도
- repeat:
    times: 3
    commands:
      - tapOn:
          id: "flaky-button"
          optional: true
```

### 6. 베스트 프랙티스

#### 테스트 독립성
```yaml
# ✅ 각 플로우는 독립적으로 실행 가능해야 함
- launchApp:
    clearState: true  # 이전 상태 초기화
```

#### 서브플로우 활용
```yaml
# ✅ 반복되는 로직은 서브플로우로
- runFlow: subflows/login.yaml

# 서브플로우 예시 (subflows/login.yaml)
appId: ${APP_ID}
---
- tapOn:
    id: "email-input"
- inputText: ${EMAIL}
- tapOn:
    id: "password-input"
- inputText: ${PASSWORD}
- tapOn:
    id: "login-button"
```

#### 환경 변수 사용
```yaml
# ✅ 하드코딩 대신 환경 변수
appId: ${APP_ID}
env:
  TEST_EMAIL: "test@example.com"
---
- inputText: ${TEST_EMAIL}

# ❌ 피해야 함
appId: com.myapp.production  # 하드코딩
```

## 리포트 포맷

```markdown
## 플로우 검증 리포트

**검증 일시**: [날짜]
**검증 파일 수**: [N]개

## 검증 결과 요약

| 레벨 | 개수 | 상태 |
|------|------|------|
| Critical | [N] | [통과/실패] |
| Major | [N] | [통과/주의] |
| Minor | [N] | [정보] |

## 파일별 상세 결과

### [파일명].yaml
**상태**: [통과/실패/주의]

#### Critical 이슈
- [ ] [라인 N] [이슈 설명]
  ```yaml
  # 문제 코드
  ```
  **해결**: [해결 방법]

#### Major 이슈
- [ ] [라인 N] [이슈 설명]

#### Minor 이슈
- [ ] [라인 N] [이슈 설명]

## 전체 개선 권장 사항

### 안정성 개선
- [ ] [파일명:라인] sleep → waitForAnimationToEnd 변경

### 베스트 프랙티스
- [ ] [설명]

## 다음 단계
1. Critical/Major 이슈 수정
2. Phase 3: 테스트 실행 진행
```

## 심각도 레벨

| 레벨 | 설명 | 예시 | 조치 |
|------|------|------|------|
| Critical | 실행 불가 | YAML 문법 오류, 잘못된 명령어 | 반드시 수정 |
| Major | 실행 가능하나 불안정 | index selector, 하드코딩된 sleep | 수정 권장 |
| Minor | 개선 가능 | 환경 변수 미사용 | 선택적 수정 |
| Info | 참고 사항 | 서브플로우 분리 제안 | 정보 제공 |

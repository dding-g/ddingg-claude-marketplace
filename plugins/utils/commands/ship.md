---
name: ship
description: Git commit, push, PR 생성을 한 번에 수행합니다. Linear issue와 연동하여 PR 제목을 자동 생성합니다.
---

변경사항을 커밋하고, 푸시한 뒤, PR을 생성해주세요.

## 1단계: Commit

1. `git add -A`로 모든 변경사항 스테이징
2. `git diff --staged`로 스테이징된 변경사항 확인
3. 변경 내용을 분석하여 conventional commit 형식으로 커밋 메시지 작성:
   - feat: 새로운 기능
   - fix: 버그 수정
   - docs: 문서 변경
   - style: 코드 포맷팅
   - refactor: 리팩토링
   - test: 테스트 추가/수정
   - chore: 빌드, 설정 변경
4. 커밋 메시지는 한글로 작성
5. 커밋 실행

## 2단계: Push

1. 현재 브랜치 확인 (`git branch --show-current`)
2. main 또는 develop 브랜치인 경우 **중단**하고 사용자에게 알림
3. `git push origin HEAD`로 현재 브랜치 푸시

## 3단계: PR 생성

### PR 제목 결정
1. 현재 브랜치 이름에서 Linear issue ID 추출 (예: `feature/ABC-123-description` → `ABC-123`)
2. Linear MCP가 사용 가능한 경우:
   - `mcp__linear__*` 도구로 해당 issue 검색
   - issue의 title을 PR 제목으로 사용
3. Linear MCP가 없거나 issue를 찾을 수 없는 경우:
   - 브랜치 이름을 기반으로 PR 제목 생성 (예: `feature/add-login` → `Add login`)

### PR 본문 작성
1. 프로젝트 루트에서 `.github/PULL_REQUEST_TEMPLATE.md` 파일 확인
2. 템플릿이 있는 경우:
   - 템플릿 형식을 따라 PR 본문 작성
   - 각 섹션에 맞는 내용 채우기
3. 템플릿이 없는 경우:
   - 커밋 내용을 요약하여 PR 본문 작성
   - 주요 변경사항을 bullet point로 나열

### PR 생성 실행
```bash
gh pr create --title "<PR 제목>" --body "<PR 본문>"
```

## 주의사항
- main, develop 브랜치에서는 실행하지 않음
- PR 생성 후 PR URL을 사용자에게 출력

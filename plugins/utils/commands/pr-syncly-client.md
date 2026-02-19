---
name: pr-syncly-client
description: Syncly Client용 PR 생성. Linear ticket 연동 및 체크리스트 자동 검증.
---

Syncly Client 프로젝트용 PR을 생성해주세요.

## 1단계: 정보 수집

1. 현재 브랜치 확인 (`git branch --show-current`)
   - `main` 또는 `staging` 브랜치이면 PR 생성 중단
2. **base 브랜치 자동 감지**:
   - `git merge-base --fork-point origin/staging HEAD`와 `git merge-base --fork-point origin/main HEAD` 실행
   - fork-point 실패 시 `git merge-base origin/staging HEAD`와 `git merge-base origin/main HEAD`로 폴백
   - merge-base 커밋이 **HEAD에 더 가까운** (더 최근인) 쪽을 base로 선택
   - 하나만 성공하면 그것을 base로 사용
   - 둘 다 실패하면 `main`을 기본값으로 사용
3. Linear Task ID 추출:
   - 브랜치 이름에서 추출 (예: `feature/ABC-123-description` → `ABC-123`)
   - 브랜치에 없으면 최근 커밋 메시지에서 `[ABC-123]` 패턴 검색
4. `git log origin/<base-branch>..HEAD --oneline`로 커밋 히스토리 확인
5. Linear MCP가 있으면 해당 ticket 내용 조회

## 2단계: 체크리스트 검증

1. **코드 스타일**: lint 검사 실행 (있으면)
2. **셀프 리뷰**: 변경된 파일 확인 (`git diff origin/<base-branch>...HEAD`)
3. **테스트 추가**: 변경 내용에 테스트가 포함되어 있는지 확인
4. **테스트 통과**: `pnpm test` 실행 (e2e 테스트 제외)
   - 테스트 실패 시 PR 생성 중단하고 사용자에게 알림

## 3단계: PR 생성

### PR 본문 작성

```markdown
## Ticket

[LINEAR_TASK_ID](https://linear.app/team/issue/LINEAR_TASK_ID)

## Description

<Linear 티켓 내용과 커밋 메시지를 참고하여 100자 이내로 요약>

## Checklist:

- [x] My code follows the code style of this project.
- [x] I have performed a self-review of my code.
- [x] I have added tests to cover my changes.
- [x] All new and existing tests pass.
```

### PR 생성 실행

```bash
gh pr create --base <base-branch> --head <branch-name> --title "<Linear 티켓 제목 또는 브랜치 기반 제목>" --body "<위 템플릿>"
```

## 4단계: 결과 반환

- PR 생성 성공 시 PR URL 출력
- 실패 시 원인 안내

## 주의사항
- main, staging, develop 브랜치에서는 실행하지 않음
- 테스트 실패 시 PR 생성하지 않음
- 반드시 `--base <base-branch> --head <branch-name>` 옵션을 사용할 것

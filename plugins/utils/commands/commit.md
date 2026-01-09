---
description: Git commit with conventional commit message
---

변경사항을 분석하고 conventional commit 형식으로 커밋해주세요.

1. `git diff --staged`로 스테이징된 변경사항 확인
2. 변경사항이 없으면 `git add -A`로 모든 변경사항 스테이징
3. 변경 내용을 분석하여 적절한 커밋 메시지 작성:
   - feat: 새로운 기능
   - fix: 버그 수정
   - docs: 문서 변경
   - style: 코드 포맷팅
   - refactor: 리팩토링
   - test: 테스트 추가/수정
   - chore: 빌드, 설정 변경
4. 커밋 메시지는 한글로 작성
5. **Co-Authored-By 줄 없이** 커밋 실행

---
name: dependencies
description: 외부 의존성 및 라이브러리를 분석합니다. 사용 중인 라이브러리, 버전, 역할을 파악합니다.
---

# Dependency Analysis

프로젝트의 외부 의존성을 분석합니다.

## 분석 항목

1. **패키지 매니저 식별**
   - npm / yarn / pnpm
   - pip / poetry / pipenv
   - 기타 패키지 매니저

2. **의존성 목록 추출**
   - Production 의존성
   - Development 의존성
   - Peer 의존성

3. **주요 의존성 분류**
   - 프레임워크 (React, Express, FastAPI 등)
   - 상태 관리 (Redux, Zustand 등)
   - 데이터 페칭 (React Query, SWR 등)
   - UI 라이브러리 (Material-UI, Tailwind 등)
   - 테스팅 (Jest, Vitest 등)
   - 빌드 도구 (Webpack, Vite 등)

4. **버전 및 호환성**
   - 구버전 패키지 확인
   - 보안 취약점 확인
   - Deprecated 패키지 확인

5. **사용 패턴 분석**
   - 주요 라이브러리 사용 위치
   - import 패턴

## 워크플로우

1. 패키지 매니저 및 lock 파일 확인
2. 의존성 목록 추출
3. 카테고리별 분류
4. 버전 현황 확인 (npm outdated 등)
5. 보안 감사 (npm audit 등)
6. 분석 리포트 생성

## 결과물

- 패키지 매니저 정보
- 주요 의존성 테이블 (버전, 역할 포함)
- 버전 현황 및 업데이트 권장 사항
- 보안 취약점 목록
- 학습 권장 라이브러리

**Agent**: `agents/dependency-analyzer.md` 사용

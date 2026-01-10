---
name: conventions
description: 코드 컨벤션 및 스타일을 분석합니다. 네이밍 규칙, 파일 구조, 코딩 스타일을 파악합니다.
---

# Convention Analysis

프로젝트의 코드 컨벤션과 스타일을 분석합니다.

## 분석 항목

1. **린트/포맷 설정**
   - ESLint / Prettier 설정
   - 들여쓰기, 따옴표, 세미콜론 규칙
   - EditorConfig 설정

2. **네이밍 컨벤션**
   - 파일명 패턴 (PascalCase, camelCase, kebab-case)
   - 변수/함수 네이밍
   - 상수 네이밍
   - 컴포넌트 네이밍

3. **디렉토리 구조 패턴**
   - 파일 타입별 vs 기능별 구조
   - 모듈 구성 방식
   - 배럴 export 패턴

4. **코드 작성 패턴**
   - 컴포넌트 작성 방식
   - 함수 선언 방식
   - import 순서
   - 타입 정의 패턴

5. **주석 및 문서화**
   - JSDoc 사용 여부
   - 인라인 주석 스타일
   - TODO/FIXME 패턴

## 워크플로우

1. 린트/포맷 설정 파일 분석
2. 파일명 패턴 샘플링
3. 코드 패턴 샘플링 (변수, 함수, 클래스)
4. import 패턴 분석
5. 주석 스타일 분석
6. 컨벤션 가이드 리포트 생성

## 결과물

- 포맷팅 규칙 테이블
- 네이밍 컨벤션 가이드
- 디렉토리 구조 패턴
- 코드 작성 예시 (Good vs Bad)
- import 순서 가이드
- 특이 사항 및 주의점

**Agent**: `agents/convention-analyzer.md` 사용

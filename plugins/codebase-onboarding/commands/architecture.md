---
name: architecture
description: 아키텍처 및 설계 패턴을 분석합니다. 레이어 구조, 모듈 의존성, 핵심 도메인을 파악합니다.
---

# Architecture Analysis

프로젝트의 아키텍처와 설계 패턴을 분석합니다.

## 분석 항목

1. **아키텍처 패턴 식별**
   - Clean Architecture / DDD / MVC / Feature-based 등
   - 레이어 분리 방식

2. **레이어 구조 분석**
   - Presentation Layer (UI, Controllers)
   - Application Layer (Use Cases, Services)
   - Domain Layer (Entities, Business Logic)
   - Infrastructure Layer (DB, External APIs)

3. **핵심 도메인 식별**
   - 주요 엔티티/모델
   - 비즈니스 로직 위치
   - 도메인 이벤트

4. **모듈 의존성 분석**
   - 모듈 간 의존 관계
   - 순환 의존성 체크
   - 레이어 역전 탐지

5. **인터페이스 분석**
   - REST API 엔드포인트
   - GraphQL 스키마
   - 내부 모듈 통신

## 워크플로우

1. 디렉토리 구조로 아키텍처 패턴 추정
2. 레이어별 파일 탐색
3. 핵심 도메인 키워드 검색
4. import/export 분석으로 의존성 파악
5. API 엔드포인트 수집
6. 아키텍처 다이어그램 및 리포트 생성

## 결과물

- 아키텍처 패턴 설명
- 레이어 구조 다이어그램
- 핵심 도메인 목록
- 모듈 의존성 그래프
- 주요 인터페이스 목록
- 설계 특이사항 및 개선 포인트

**Agent**: `agents/architecture-analyzer.md` 사용

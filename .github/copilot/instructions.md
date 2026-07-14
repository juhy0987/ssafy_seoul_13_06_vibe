# GitHub Copilot Instructions — LocalHub (서울)

이 저장소는 공공데이터 기반 서울 지역 정보 공유 커뮤니티 **LocalHub**를 개발한다.
코드/제안을 생성하기 전에 **`.ai/` 룰셋을 우선 준수**한다.

## 룰셋 진입점 (우선순위 순)
1. [프로젝트 컨텍스트](../../.ai/01-project-context.md) — 범위 · 기술 스택 · MVP
2. [하드 제약(위반 시 미완료)](../../.ai/02-constraints.md) — 보안 · 정책 · 비용 · 납기
3. [챗봇 프롬프트 룰셋](../../.ai/03-chatbot-prompts.md) — `POST /api/chat` 프롬프트 규격

> `.ai/` 문서와 아래 요약이 충돌하면 **`.ai/` 문서가 우선**한다.
> `02-constraints.md`의 항목은 어떤 경우에도 변경·완화·우회하지 않는다.

## 절대 규칙 (요약)
- 기술 스택 고정: **Vue.js 3 (SPA) + FastAPI + SQLAlchemy + SQLite**. 임의 변경 금지.
- 인증 없음(익명). 게시글 수정/삭제는 **평문 비밀번호 일치**로만 검증 — 해싱·암호화 추가 금지(의도된 설계).
- API 키·DB 경로 등 민감정보는 **`.env`만** 사용. 코드/커밋 하드코딩 금지. `.env`는 `.gitignore`에 포함.
- 챗봇은 **제공 JSON에만 근거**. 직접 공공 API 호출 금지. LLM은 `gpt-5-mini`(OpenAI), **토큰/예산 최소화**.
- **평문 비밀번호 등 민감 컬럼은 절대 LLM 컨텍스트에 넣지 않는다** (03 문서 보안 규칙).
- 개발 착수 후 범위 변경 금지. MVP 범위(01 문서) 밖 기능은 제안하지 않는다.

## 코드 컨벤션
- **백엔드**: FastAPI 라우터-서비스 계층 분리, Pydantic 스키마, SQLAlchemy ORM. 챗봇 프롬프트 문자열은 하드코딩하지 말고 `backend/app/prompts/`로 외부화(03 문서를 정본으로 동기화).
- **프론트**: Vue 3 `<script setup>` + Composition API + Vue Router, 컴포넌트 단위 분리.
- 키·시크릿을 로그·응답·커밋에 출력하지 않는다.

> FE/BE를 별도 저장소로 분리 제출하는 경우, 이 파일을 각 저장소 루트의 `.github/copilot/instructions.md`로 복제하고 `.ai/` 룰셋도 함께 동봉한다.

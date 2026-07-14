# .ai — LocalHub AI 룰셋

이 폴더는 LocalHub 개발 시 **AI(코딩 어시스턴트 · 런타임 챗봇)가 지켜야 할 규칙의 정본(正本)**이다.
진입점은 [`.github/copilot/instructions.md`](../.github/copilot/instructions.md)이며, 그 파일이 아래 문서를 참조한다.

## 구성 (우선순위 순)
| 파일 | 내용 |
|---|---|
| [`01-project-context.md`](01-project-context.md) | 서비스 개요·기술 스택·MVP 범위(MoSCoW)·산출물 |
| [`02-constraints.md`](02-constraints.md) | 하드 제약(위반 시 미완료) — 보안·비밀정보·비용·범위·납기 |
| [`03-chatbot-prompts.md`](03-chatbot-prompts.md) | `POST /api/chat` 챗봇 프롬프트 룰셋(gpt-5-mini) |

## 사용 규칙
- 문서 간 충돌 시 **번호가 낮은 문서 > 높은 문서**, `02-constraints.md`는 어떤 경우에도 우선한다.
- `02-constraints.md`의 항목은 변경·완화·우회하지 않는다.
- 런타임 챗봇 프롬프트는 코드에 하드코딩하지 말고 `backend/app/prompts/`로 외부화하고, `03` 문서를 정본으로 동기화한다.

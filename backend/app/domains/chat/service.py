from app.domains.posts import service as posts
from app.domains.tourism import service as tourism
from app.domains.chat.rag import chain as rag

def reply(message: str, history: list[dict] | None = None) -> str:
    history = history or []
    try:
        return rag.answer(message, history)
    except Exception:
        # RAG 미구성(의존성 미설치·임베딩 미적재·API 키 부재 등) 시 키워드 검색으로 폴백
        return _keyword_reply(message, history)


def _keyword_reply(message: str, history: list[dict]) -> str:
    spot_matches = tourism.search_spots(message, history)
    post_matches = posts.search_posts(message, limit=3)
    if not spot_matches and not post_matches:
        keywords = tourism.tokenize(message)
        if keywords:
            return f"서울에서 '{keywords[0]}'와 잘 맞는 정보를 찾지 못했어요. 다른 키워드로 다시 물어봐 주세요."
        return '서울 관광지·문화시설·축제 정보나 커뮤니티 게시글을 물어보면 찾아드릴게요.'

    lines = ['서울에서 찾은 정보예요:']
    for category, spot in spot_matches:
        address = spot.get('address') or '주소 정보 없음'
        lines.append(f"- [{tourism.data_label(category)}] {spot.get('title')} · {address}")
    for post in post_matches:
        lines.append(f"- [게시글] {post['title']} (장소: {post['spot_name']})")
    return '\n'.join(lines)

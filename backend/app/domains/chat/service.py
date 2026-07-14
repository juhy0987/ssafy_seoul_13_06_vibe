from app.domains.tourism import service as tourism


def reply(message: str, history: list[dict] | None = None) -> str:
    matches = tourism.search_spots(message, history)
    if not matches:
        keywords = tourism.tokenize(message)
        if keywords:
            return f"서울에서 '{keywords[0]}'와 잘 맞는 장소를 찾지 못했어요. 다른 키워드로 다시 물어봐 주세요."
        return '서울 관광지, 문화시설, 축제 정보를 물어보면 바로 찾아드릴게요.'

    lines = ['서울에서 추천할 만한 곳을 찾았어요:']
    for dataset, item in matches:
        address = item.get('address') or '주소 정보 없음'
        lines.append(f"- [{tourism.data_label(dataset)}] {item.get('title')} · {address}")
    return '\n'.join(lines)

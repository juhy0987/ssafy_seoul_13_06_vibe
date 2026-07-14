from functools import lru_cache
from pathlib import Path
import json
import re

from fastapi import HTTPException, status

from app.domains.tourism import schemas


DATASET_FILES = {
    'attractions': 'attractions.json',
    'culture': 'culture.json',
    'festivals': 'festivals.json',
}

DATA_ROOT = Path(__file__).resolve().parents[4] / 'frontend' / 'public' / 'data' / 'seoul'


def _dataset_path(dataset: str) -> Path:
    filename = DATASET_FILES.get(dataset)
    if not filename:
        raise HTTPException(status.HTTP_404_NOT_FOUND, '지원하지 않는 관광 데이터셋입니다.')
    return DATA_ROOT / filename


@lru_cache(maxsize=len(DATASET_FILES))
def _load_dataset(dataset: str) -> dict:
    path = _dataset_path(dataset)
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def list_spots(dataset: str, limit: int = 6, with_image_only: bool = True) -> schemas.SpotListResponse:
    data = _load_dataset(dataset)
    items = data['items']
    if with_image_only:
        items = [item for item in items if item.get('thumbnail') or item.get('image')]

    limited = items[:limit]
    return schemas.SpotListResponse(
        region=data['region'],
        contentType=data['contentType'],
        contentTypeId=data['contentTypeId'],
        total=data['total'],
        included=len(limited),
        items=limited,
    )


def get_dataset_meta(dataset: str) -> schemas.SpotMetaResponse:
    data = _load_dataset(dataset)
    return schemas.SpotMetaResponse(
        region=data['region'],
        contentType=data['contentType'],
        contentTypeId=data['contentTypeId'],
        total=data['total'],
    )


def _tokenize(text: str) -> list[str]:
    stopwords = {
        '서울', '서울시', '서울의', '근처', '주변', '알려줘', '알려주세요', '추천', '가볼', '만한',
        '어디', '어떤', '있어', '있나요', '보여줘', '찾아줘', '한', '곳', '곳을', '명소', '정보',
    }
    tokens = [token for token in re.findall(r'[0-9A-Za-z가-힣]+', text.lower()) if len(token) > 1]
    return [token for token in tokens if token not in stopwords]


def _dataset_priority(message: str) -> list[str]:
    priority = []
    if any(keyword in message for keyword in ('축제', '행사', '공연')):
        priority.append('festivals')
    if any(keyword in message for keyword in ('문화', '실내', '박물관', '미술관', '전시')):
        priority.append('culture')
    if any(keyword in message for keyword in ('관광', '명소', '여행', '산책', '공원', '궁', '한강')):
        priority.append('attractions')
    for dataset in DATASET_FILES:
        if dataset not in priority:
            priority.append(dataset)
    return priority


def _score_item(item: dict, keywords: list[str]) -> int:
    haystack = ' '.join(filter(None, [item.get('title', ''), item.get('address', '')]))
    return sum(1 for keyword in keywords if keyword in haystack)


def search_spots(message: str, history: list[dict] | None = None, limit: int = 3) -> list[tuple[str, dict]]:
    keywords = _tokenize(message)
    if len(keywords) < 2 and history:
        last_user = next((entry.get('content', '') for entry in reversed(history) if entry.get('role') == 'user'), '')
        keywords.extend(token for token in _tokenize(last_user) if token not in keywords)

    prioritized = _dataset_priority(message)
    matches: list[tuple[int, str, dict]] = []

    for dataset in prioritized:
        data = _load_dataset(dataset)
        for item in data['items']:
            score = _score_item(item, keywords) if keywords else 0
            if keywords and score == 0:
                continue
            matches.append((score, dataset, item))

    matches.sort(key=lambda entry: (-entry[0], entry[2].get('title', '')))
    return [(dataset, item) for _, dataset, item in matches[:limit]]


def data_label(dataset: str) -> str:
    return {
        'attractions': '관광지',
        'culture': '문화시설',
        'festivals': '축제·행사',
    }[dataset]


def build_chat_reply(message: str, history: list[dict] | None = None) -> str:
    keywords = _tokenize(message)
    matches = search_spots(message, history)
    if not matches:
        if keywords:
            return f"서울에서 '{keywords[0]}'와 잘 맞는 장소를 찾지 못했어요. 다른 키워드로 다시 물어봐 주세요."
        return '서울 관광지, 문화시설, 축제 정보를 물어보면 바로 찾아드릴게요.'

    lines = ['서울에서 추천할 만한 곳을 찾았어요:']
    for dataset, item in matches:
        address = item.get('address') or '주소 정보 없음'
        lines.append(f"- [{data_label(dataset)}] {item.get('title')} · {address}")
    return '\n'.join(lines)

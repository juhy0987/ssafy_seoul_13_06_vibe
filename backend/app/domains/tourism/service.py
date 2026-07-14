from functools import lru_cache
from pathlib import Path
import json
import re

from fastapi import HTTPException, status

from app.domains.tourism import schemas

# 단일 데이터 원천: 제공 공공데이터(서울) — backend 내부로 자기완결
SEOUL_DATA_ROOT = Path(__file__).resolve().parents[3] / 'data' / '서울'

# /api/spots 는 프론트 계약(영문 dataset 키)을 유지하고, 내부적으로 카테고리에 매핑한다.
DATASET_ALIAS = {
    'attractions': '관광지',
    'culture': '문화시설',
    'festivals': '축제공연행사',
}

# 챗봇이 검색하는 카테고리
CHAT_CATEGORIES = ('관광지', '문화시설', '축제공연행사')


def _category_of(dataset: str) -> str:
    category = DATASET_ALIAS.get(dataset)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, '지원하지 않는 관광 데이터셋입니다.')
    return category


@lru_cache(maxsize=None)
def _load(category: str) -> dict:
    path = SEOUL_DATA_ROOT / f'서울_{category}.json'
    with path.open(encoding='utf-8') as handle:
        return json.load(handle)


def _as_float(value) -> float | None:
    try:
        return float(value) if value not in (None, '') else None
    except (TypeError, ValueError):
        return None


def _to_spot(item: dict) -> dict:
    return {
        'id': str(item['contentid']),
        'title': item.get('title'),
        'address': item.get('addr1') or None,
        'tel': item.get('tel') or None,
        'image': item.get('firstimage') or None,
        'thumbnail': item.get('firstimage2') or item.get('firstimage') or None,
        'lat': _as_float(item.get('mapy')),
        'lng': _as_float(item.get('mapx')),
    }


@lru_cache(maxsize=None)
def _spots(category: str) -> list[dict]:
    return [_to_spot(item) for item in _load(category)['items']]


@lru_cache(maxsize=None)
def _name_index(category: str) -> dict[str, str]:
    return {spot['id']: spot['title'] for spot in _spots(category)}


def list_spots(dataset: str, limit: int = 6, with_image_only: bool = True) -> schemas.SpotListResponse:
    category = _category_of(dataset)
    data = _load(category)
    spots = _spots(category)
    if with_image_only:
        spots = [spot for spot in spots if spot['thumbnail'] or spot['image']]
    return schemas.SpotListResponse(
        region=data['region'],
        contentType=data['contentType'],
        contentTypeId=data['contentTypeId'],
        total=data['total'],
        items=spots[:limit],
    )


def get_dataset_meta(dataset: str) -> schemas.SpotMetaResponse:
    data = _load(_category_of(dataset))
    return schemas.SpotMetaResponse(
        region=data['region'],
        contentType=data['contentType'],
        contentTypeId=data['contentTypeId'],
        total=data['total'],
    )


def get_spot_name(category: str, spot_id: str) -> str | None:
    """카테고리 데이터에서 spot_id(contentid)에 해당하는 장소명을 반환. 없으면 None."""
    return _name_index(category).get(spot_id)


def tokenize(text: str) -> list[str]:
    stopwords = {
        '서울', '서울시', '서울의', '근처', '주변', '알려줘', '알려주세요', '추천', '가볼', '만한',
        '어디', '어떤', '있어', '있나요', '보여줘', '찾아줘', '한', '곳', '곳을', '명소', '정보',
    }
    tokens = [token for token in re.findall(r'[0-9A-Za-z가-힣]+', text.lower()) if len(token) > 1]
    return [token for token in tokens if token not in stopwords]


def _category_priority(message: str) -> list[str]:
    priority = []
    if any(keyword in message for keyword in ('축제', '행사', '공연')):
        priority.append('축제공연행사')
    if any(keyword in message for keyword in ('문화', '실내', '박물관', '미술관', '전시')):
        priority.append('문화시설')
    if any(keyword in message for keyword in ('관광', '명소', '여행', '산책', '공원', '궁', '한강')):
        priority.append('관광지')
    for category in CHAT_CATEGORIES:
        if category not in priority:
            priority.append(category)
    return priority


def _score_spot(spot: dict, keywords: list[str]) -> int:
    haystack = ' '.join(filter(None, [spot.get('title', ''), spot.get('address', '')]))
    return sum(1 for keyword in keywords if keyword in haystack)


def search_spots(message: str, history: list[dict] | None = None, limit: int = 3) -> list[tuple[str, dict]]:
    keywords = tokenize(message)
    if len(keywords) < 2 and history:
        last_user = next((entry.get('content', '') for entry in reversed(history) if entry.get('role') == 'user'), '')
        keywords.extend(token for token in tokenize(last_user) if token not in keywords)

    matches: list[tuple[int, str, dict]] = []
    for category in _category_priority(message):
        for spot in _spots(category):
            score = _score_spot(spot, keywords) if keywords else 0
            if keywords and score == 0:
                continue
            matches.append((score, category, spot))

    matches.sort(key=lambda entry: (-entry[0], entry[2].get('title', '')))
    return [(category, spot) for _, category, spot in matches[:limit]]


def data_label(category: str) -> str:
    return {'축제공연행사': '축제·행사'}.get(category, category)

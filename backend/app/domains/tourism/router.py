from fastapi import APIRouter, Query

from app.domains.tourism import schemas, service


router = APIRouter(prefix='/api/spots', tags=['tourism'])


@router.get('/summary', response_model=schemas.SpotSummaryResponse, summary='전체 관광 데이터 개수 합계')
def get_summary():
    # 주의: '/{dataset}' 보다 먼저 선언해야 'summary' 가 dataset 으로 잡히지 않는다.
    return service.get_summary()


@router.get('/{dataset}', response_model=schemas.SpotListResponse, summary='관광 데이터 목록 조회')
def list_spots(
    dataset: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
    with_image_only: bool = Query(default=True),
):
    return service.list_spots(dataset, page=page, size=size, with_image_only=with_image_only)


@router.get('/{dataset}/meta', response_model=schemas.SpotMetaResponse, summary='관광 데이터 메타 조회')
def get_dataset_meta(dataset: str):
    return service.get_dataset_meta(dataset)


@router.get('/{dataset}/random', response_model=schemas.SpotListResponse, summary='카테고리별 랜덤 장소 추출')
def random_spots(
    dataset: str,
    size: int = Query(default=50, ge=1, le=50),
    with_image_only: bool = Query(default=True),
):
    return service.random_spots(dataset, size=size, with_image_only=with_image_only)

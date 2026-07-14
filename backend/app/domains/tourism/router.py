from fastapi import APIRouter, Query

from app.domains.tourism import schemas, service


router = APIRouter(prefix='/api/spots', tags=['tourism'])


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

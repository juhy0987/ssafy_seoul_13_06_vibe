from fastapi import APIRouter, Query

from app.domains.tourism import schemas, service


router = APIRouter(prefix='/api/spots', tags=['tourism'])


@router.get('/{dataset}', response_model=schemas.SpotListResponse, summary='관광 데이터 목록 조회')
def list_spots(
    dataset: str,
    limit: int = Query(default=6, ge=0, le=50),
    with_image_only: bool = Query(default=True),
):
    return service.list_spots(dataset, limit=limit, with_image_only=with_image_only)


@router.get('/{dataset}/meta', response_model=schemas.SpotMetaResponse, summary='관광 데이터 메타 조회')
def get_dataset_meta(dataset: str):
    return service.get_dataset_meta(dataset)

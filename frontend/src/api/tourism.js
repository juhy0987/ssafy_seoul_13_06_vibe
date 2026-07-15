import { request } from './client'
import { toApiCategory } from '@/config/region'

/**
 * 백엔드가 서울 관광 데이터를 내려준다.
 * 백엔드 목록 파라미터는 page·size 이므로 limit 을 size 로 매핑한다.
 * (기존엔 limit 을 보냈으나 백엔드가 인식하지 못해 항상 기본 size=10 이 적용됐다.)
 */
export async function listSpots(dataset, { limit = 6, page = 1, withImageOnly = true } = {}) {
  return request(`/spots/${dataset}`, {
    params: { page, size: limit, with_image_only: withImageOnly },
  })
}

/**
 * 게시판 카테고리(slug)에 해당하는 장소 목록을 불러온다.
 * 백엔드의 영문 dataset alias 는 일부(관광지·문화시설·축제)만 지원하므로,
 * 모든 카테고리에서 동작하도록 한글 카테고리명을 dataset 으로 전달한다.
 */
export async function listSpotsForCategory(categorySlug, { limit = 50 } = {}) {
  return listSpots(toApiCategory(categorySlug), { limit, withImageOnly: false })
}

export async function getDatasetMeta(dataset) {
  return request(`/spots/${dataset}/meta`)
}

/** 전체 카테고리 장소 수 합계(+카테고리별 내역). 백엔드가 한 번에 집계해준다. */
export async function getSpotsSummary() {
  return request('/spots/summary')
}

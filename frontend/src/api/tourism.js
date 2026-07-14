import { request } from './client'

/** 백엔드가 서울 관광 데이터를 내려준다. */
export async function listSpots(dataset, { limit = 6, withImageOnly = true } = {}) {
  return request(`/spots/${dataset}`, { params: { limit, with_image_only: withImageOnly } })
}

export async function getDatasetMeta(dataset) {
  return request(`/spots/${dataset}/meta`)
}

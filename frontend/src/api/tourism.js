/**
 * 서울 권역 공공데이터(TourAPI 4.0) 조회.
 *
 * 현 단계에서는 scripts/prepare-data.mjs 로 가공한 정적 JSON(public/data/seoul/)을 읽는다.
 * 백엔드가 완성되면 이 모듈의 fetch 대상만 /api/spots 로 바꾸면 화면은 그대로 동작한다.
 */
const cache = new Map()

async function loadDataset(name) {
  if (cache.has(name)) return cache.get(name)

  const promise = fetch(`${import.meta.env.BASE_URL}data/seoul/${name}.json`)
    .then((res) => {
      if (!res.ok) throw new Error(`${name} 데이터를 불러오지 못했습니다 (${res.status})`)
      return res.json()
    })
    .catch((err) => {
      cache.delete(name)
      throw err
    })

  cache.set(name, promise)
  return promise
}

/** 대표 이미지가 있는 항목만, 요청한 개수만큼 반환한다. */
export async function listSpots(dataset, { limit = 6, withImageOnly = true } = {}) {
  const data = await loadDataset(dataset)
  const items = withImageOnly ? data.items.filter((item) => item.image) : data.items
  return items.slice(0, limit)
}

export async function getDatasetMeta(dataset) {
  const data = await loadDataset(dataset)
  return { total: data.total, contentType: data.contentType, region: data.region }
}

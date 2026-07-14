/**
 * 제공된 서울 권역 원본 JSON(TourAPI 4.0)에서 화면에 필요한 필드만 추려
 * public/data/seoul/*.json 으로 저장한다.
 *
 * 원본은 서울_쇼핑.json 이 4MB에 달해 그대로 번들에 넣을 수 없다.
 * 백엔드가 완성되면 이 스크립트 대신 FastAPI 가 같은 형태의 응답을 내려주면 된다.
 *
 * 실행: npm run prepare:data
 */
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const SOURCE_DIR = resolve(HERE, '../../../data/서울')
const OUT_DIR = resolve(HERE, '../public/data/seoul')

// 화면에 노출되는 데이터셋만 가공한다. (원본 파일명 → 출력 파일명)
const DATASETS = [
  { source: '서울_관광지.json', out: 'attractions', limit: 120 },
  { source: '서울_문화시설.json', out: 'culture', limit: 120 },
  { source: '서울_축제공연행사.json', out: 'festivals', limit: 120 },
]

/** 이미지가 있는 항목을 앞으로 보내고, 그 안에서는 최근 수정순으로 정렬한다. */
function rank(a, b) {
  const imageDiff = Number(Boolean(b.firstimage)) - Number(Boolean(a.firstimage))
  if (imageDiff !== 0) return imageDiff
  return String(b.modifiedtime).localeCompare(String(a.modifiedtime))
}

function toSpot(item) {
  return {
    id: item.contentid,
    contentTypeId: item.contenttypeid,
    title: item.title,
    address: item.addr1 || '',
    tel: item.tel || '',
    image: item.firstimage || '',
    thumbnail: item.firstimage2 || item.firstimage || '',
    lat: item.mapy ? Number(item.mapy) : null,
    lng: item.mapx ? Number(item.mapx) : null,
    modifiedAt: item.modifiedtime || '',
  }
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true })

  for (const { source, out, limit } of DATASETS) {
    const raw = JSON.parse(await readFile(join(SOURCE_DIR, source), 'utf-8'))
    const items = [...raw.items].sort(rank).slice(0, limit).map(toSpot)

    const payload = {
      region: raw.region,
      contentType: raw.contentType,
      contentTypeId: raw.contentTypeId,
      total: raw.total, // 원본 전체 건수 (화면에 "783곳" 처럼 표기)
      included: items.length,
      items,
    }

    const target = join(OUT_DIR, `${out}.json`)
    await writeFile(target, JSON.stringify(payload), 'utf-8')
    console.log(`OK ${out}.json - ${items.length}건 (원본 ${raw.total}건)`)
  }
}

main().catch((err) => {
  console.error('데이터 가공 실패:', err.message)
  process.exitCode = 1
})

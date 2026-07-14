/**
 * 선정 권역과 게시판 카테고리 정의.
 *
 * 카테고리 slug 는 라우트(/board/:category)와 백엔드 posts.category 컬럼에
 * 그대로 쓰이므로 영문 소문자로 고정한다.
 *
 * 서울 권역 제공 데이터에는 음식점(contenttypeid=39) 파일이 없어
 * 의뢰서 와이어프레임의 '맛집' 자리를 '문화시설'로 대체했다.
 */
export const REGION = {
  name: '서울',
  nameEn: 'Seoul',
  tagline: '서울 지역 정보를 한눈에',
  description: '관광지 · 문화시설 · 축제 정보를 익명으로 나눠보세요',
}

export const CATEGORIES = [
  {
    slug: 'attraction',
    label: '관광지',
    icon: '⛩',
    contentTypeId: '12',
    dataset: 'attractions',
    description: '고궁·공원·명소 이야기',
  },
  {
    slug: 'culture',
    label: '문화시설',
    icon: '🏛',
    contentTypeId: '14',
    dataset: 'culture',
    description: '미술관·박물관·공연장',
  },
  {
    slug: 'festival',
    label: '축제·행사',
    icon: '🎆',
    contentTypeId: '15',
    dataset: 'festivals',
    description: '지금 열리는 축제와 행사',
  },
]

export const CATEGORY_BY_SLUG = Object.fromEntries(CATEGORIES.map((c) => [c.slug, c]))

export function findCategory(slug) {
  return CATEGORY_BY_SLUG[slug] ?? null
}

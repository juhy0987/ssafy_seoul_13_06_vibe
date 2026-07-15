/**
 * 선정 권역과 게시판 카테고리 정의.
 *
 * 카테고리 slug 는 라우트(/board/:category)와 백엔드 posts.category 컬럼에
 * 그대로 쓰이므로 영문 소문자로 고정한다.
 *
 * contentTypeId 는 TourAPI 콘텐츠 타입 기준(관광지 12 · 문화시설 14 ·
 * 축제공연행사 15 · 여행코스 25 · 레포츠 28 · 숙박 32 · 쇼핑 38).
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
    slug: 'leisure',
    label: '레포츠',
    icon: '🏄',
    contentTypeId: '28',
    dataset: 'leisure',
    description: '등산·수상·액티비티 정보',
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
    slug: 'shopping',
    label: '쇼핑',
    icon: '🛍',
    contentTypeId: '38',
    dataset: 'shopping',
    description: '전통시장·거리·아울렛',
  },
  {
    slug: 'lodging',
    label: '숙박',
    icon: '🛏',
    contentTypeId: '32',
    dataset: 'lodging',
    description: '호텔·게스트하우스 후기',
  },
  {
    slug: 'course',
    label: '여행코스',
    icon: '🗺',
    contentTypeId: '25',
    dataset: 'courses',
    description: '테마별 추천 코스',
  },
  {
    slug: 'festival',
    label: '축제행사',
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

/**
 * 백엔드 posts.category(enum)와 TourAPI 관광 카테고리는 모두 한글 값을 쓴다.
 * 프론트는 영문 slug 로 동작하므로 API 경계에서 아래 표로 상호 변환한다.
 * (festival 은 표시 라벨 '축제행사' 와 백엔드 값 '축제공연행사' 가 달라 명시적으로 매핑)
 */
const API_CATEGORY_BY_SLUG = {
  attraction: '관광지',
  leisure: '레포츠',
  culture: '문화시설',
  shopping: '쇼핑',
  lodging: '숙박',
  course: '여행코스',
  festival: '축제공연행사',
}

const SLUG_BY_API_CATEGORY = Object.fromEntries(
  Object.entries(API_CATEGORY_BY_SLUG).map(([slug, value]) => [value, slug]),
)

/** slug → 백엔드/TourAPI 한글 카테고리(게시글 category · 관광 dataset 공용) */
export function toApiCategory(slug) {
  return API_CATEGORY_BY_SLUG[slug] ?? slug
}

/** 백엔드 한글 카테고리 → 프론트 slug */
export function toCategorySlug(apiCategory) {
  return SLUG_BY_API_CATEGORY[apiCategory] ?? apiCategory
}

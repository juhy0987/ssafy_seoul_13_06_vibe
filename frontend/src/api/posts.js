import { request } from './client'
import { MOCK_POSTS } from './mock/posts'
import { toApiCategory, toCategorySlug } from '@/config/region'

/**
 * 백엔드가 아직 없을 때는 목 데이터로 폴백한다.
 * FastAPI 가 붙으면 이 폴백은 그대로 두고 정상 응답만 흐르게 되므로,
 * 별도 코드 수정 없이 실서버로 전환된다.
 */
async function withMockFallback(fn, fallback) {
  try {
    return await fn()
  } catch (err) {
    if (import.meta.env.DEV) {
      console.info('[LocalHub] 백엔드 응답 없음 — 목 데이터로 표시합니다.', err.message)
    }
    return fallback()
  }
}

/**
 * 백엔드는 category 를 한글 enum(관광지 등)으로 주고받는다.
 * 프론트 전역은 영문 slug 를 쓰므로 응답을 받을 때 slug 로 정규화한다.
 */
function normalizePost(post) {
  if (!post) return post
  return { ...post, category: toCategorySlug(post.category) }
}

function paginate(items, page, size) {
  const start = (page - 1) * size
  return {
    items: items.slice(start, start + size),
    total: items.length,
    page,
    size,
  }
}

export function listPosts({ category, q = '', page = 1, size = 10 } = {}) {
  return withMockFallback(
    () =>
      request('/posts', {
        // slug → 백엔드 한글 카테고리로 변환해 전달
        params: { category: category ? toApiCategory(category) : undefined, q, page, size },
      }).then((res) => ({ ...res, items: res.items.map(normalizePost) })),
    () => {
      const keyword = q.trim().toLowerCase()
      const filtered = MOCK_POSTS.filter((p) => {
        const matchCategory = !category || p.category === category
        const matchKeyword =
          !keyword ||
          p.title.toLowerCase().includes(keyword) ||
          p.content.toLowerCase().includes(keyword)
        return matchCategory && matchKeyword
      })
      return paginate(filtered, page, size)
    },
  )
}

export function listRecentPosts(limit = 5) {
  return withMockFallback(
    () =>
      request('/posts', { params: { page: 1, size: limit } }).then((res) =>
        res.items.map(normalizePost),
      ),
    () => MOCK_POSTS.slice(0, limit),
  )
}

export function getPost(id) {
  return withMockFallback(
    () => request(`/posts/${id}`).then(normalizePost),
    () => MOCK_POSTS.find((p) => p.id === Number(id)) ?? null,
  )
}

/** 폼에서 넘어온 payload 의 category(slug) 를 백엔드 한글 값으로 변환한다. */
function toApiPayload(payload) {
  return { ...payload, category: toApiCategory(payload.category) }
}

export function createPost(payload) {
  return request('/posts', { method: 'POST', body: toApiPayload(payload) }).then(normalizePost)
}

export function updatePost(id, payload) {
  return request(`/posts/${id}`, { method: 'PUT', body: toApiPayload(payload) }).then(normalizePost)
}

export function deletePost(id, password) {
  return request(`/posts/${id}`, { method: 'DELETE', body: { password } })
}

/**
 * 수정 화면 진입 전 비밀번호 검증. 성공 시 204, 불일치 시 403(ApiError)을 던진다.
 * 백엔드 POST /api/posts/{id}/verify 를 사용한다.
 */
export function verifyPassword(id, password) {
  return request(`/posts/${id}/verify`, { method: 'POST', body: { password } })
}

import { request } from './client'
import { MOCK_POSTS } from './mock/posts'

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
    () => request('/posts', { params: { category, q, page, size } }),
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
    () => request('/posts', { params: { page: 1, size: limit } }).then((res) => res.items),
    () => MOCK_POSTS.slice(0, limit),
  )
}

export function getPost(id) {
  return withMockFallback(
    () => request(`/posts/${id}`),
    () => MOCK_POSTS.find((p) => p.id === Number(id)) ?? null,
  )
}

export function createPost(payload) {
  return request('/posts', { method: 'POST', body: payload })
}

export function updatePost(id, payload) {
  return request(`/posts/${id}`, { method: 'PUT', body: payload })
}

export function deletePost(id, password) {
  return request(`/posts/${id}`, { method: 'DELETE', body: { password } })
}

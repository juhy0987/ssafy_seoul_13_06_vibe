const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/**
 * FastAPI 백엔드 호출 래퍼.
 * 백엔드가 아직 없는 단계에서는 요청이 실패하므로, 호출부에서 목 데이터로 폴백한다.
 */
export async function request(path, { method = 'GET', body, params, signal } = {}) {
  const url = new URL(`${BASE_URL}${path}`, window.location.origin)
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, value)
      }
    }
  }

  const res = await fetch(url, {
    method,
    signal,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })

  if (!res.ok) {
    let detail = `요청에 실패했습니다 (${res.status})`
    try {
      const data = await res.json()
      if (data?.detail) detail = data.detail
    } catch {
      /* 응답 본문이 JSON이 아니면 기본 메시지를 쓴다 */
    }
    throw new ApiError(detail, res.status)
  }

  if (res.status === 204) return null
  return res.json()
}

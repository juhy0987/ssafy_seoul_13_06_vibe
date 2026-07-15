import { request } from './client'

/**
 * 댓글 API — 게시글에 종속(/api/posts/{postId}/comments).
 * 게시글과 동일하게 익명 + 평문 비밀번호 방식(수정·삭제 시 비밀번호 필요).
 */
export function listComments(postId) {
  return request(`/posts/${postId}/comments`)
}

export function createComment(postId, { content, password }) {
  return request(`/posts/${postId}/comments`, { method: 'POST', body: { content, password } })
}

export function updateComment(postId, commentId, { content, password }) {
  return request(`/posts/${postId}/comments/${commentId}`, {
    method: 'PUT',
    body: { content, password },
  })
}

export function deleteComment(postId, commentId, password) {
  return request(`/posts/${postId}/comments/${commentId}`, {
    method: 'DELETE',
    body: { password },
  })
}

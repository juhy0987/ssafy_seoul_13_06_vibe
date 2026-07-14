import { request } from './client'

/**
 * POST /api/chat — 제공 JSON 기반 자연어 지역 정보 질의응답.
 * 백엔드가 없으면 안내 메시지를 돌려주어 UI 흐름은 그대로 확인할 수 있게 한다.
 */
export async function sendChatMessage(message, history = []) {
  try {
    const res = await request('/chat', {
      method: 'POST',
      body: { message, history },
    })
    return res.reply
  } catch {
    return '아직 챗봇 서버(FastAPI /api/chat)가 연결되지 않았어요. 백엔드를 실행하면 서울 관광지·축제 정보를 답변해 드립니다.'
  }
}

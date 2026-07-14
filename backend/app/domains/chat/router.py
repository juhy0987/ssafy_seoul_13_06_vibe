from fastapi import APIRouter

from app.domains.chat import schemas, service


router = APIRouter(prefix='/api/chat', tags=['chat'])


@router.post('', response_model=schemas.ChatResponse, summary='지역 정보 챗봇 응답')
def send_message(payload: schemas.ChatRequest):
    history = [entry.model_dump() for entry in payload.history]
    return schemas.ChatResponse(reply=service.reply(payload.message, history))

from app.domains.tourism import service as tourism_service


def reply(message: str, history: list[dict] | None = None) -> str:
    return tourism_service.build_chat_reply(message, history)

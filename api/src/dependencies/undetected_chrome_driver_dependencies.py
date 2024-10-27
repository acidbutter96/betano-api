from typing import Any, Coroutine

from api.src.services import SuperBetBotService


async def get_superbet_bot_service_dependency() -> Coroutine[SuperBetBotService, None, Any]:
    superbet_bot_service = SuperBetBotService()
    return superbet_bot_service

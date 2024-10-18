from typing import Any, Coroutine

from src.services import BetanoBotService
# import chromedriver_autoinstaller as chromedriver
# chromedriver.install()


async def get_betano_bot_service_dependency() -> Coroutine[BetanoBotService, None, Any]:
    betano_bot_service = BetanoBotService()
    return betano_bot_service

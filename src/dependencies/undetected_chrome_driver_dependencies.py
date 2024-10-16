from typing import Any, Coroutine

from src.services import BetanoBotService
from undetected_chromedriver import Chrome
# import chromedriver_autoinstaller as chromedriver
# chromedriver.install()


async def get_undetected_chrome_driver_dependency() -> Coroutine[Chrome, None, Any]:
    betano_bot_service = BetanoBotService()
    return betano_bot_service.driver

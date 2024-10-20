from src.services import BetanoBotService
import asyncio


betano_bot_service = BetanoBotService()

asyncio.run(betano_bot_service.get_session_and_print())

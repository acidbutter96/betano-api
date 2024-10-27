from api.src.services import SuperBetBotService
import asyncio


superbet_bot_service = SuperBetBotService()

asyncio.run(superbet_bot_service.get_session_and_print())

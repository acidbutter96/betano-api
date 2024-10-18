from fastapi import FastAPI
from src.api import router
import platform
import asyncio

# Apply event loop policy for Windows
if platform.system() == "Windows":
    import nest_asyncio
    nest_asyncio.apply()  # Allow nested event loops (useful in some async contexts)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_api() -> FastAPI:
    application = FastAPI(
        title="Betano Bot Application",
        description="API for managing and interacting with the Betano bot",
        version="1.0.0",
        openapi_url="/api",
        docs_url="/",
        redoc_url=False,  # Disable ReDoc
    )

    application.include_router(router)
    return application


app = get_api()

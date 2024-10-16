from fastapi import FastAPI
from src.api import router


def get_api() -> FastAPI:
    application = FastAPI(
        title="Betano Bot Application",
        description="API for managing and interacting with the Betano bot",
        version="1.0.0",
        openapi_url="/api",
        docs_url="/",
        redoc_url=False,  # To disable ReDoc
    )

    application.include_router(router)

    return application


app = get_api()

import redis
from uuid import uuid4

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from api.src.models import SuperBetLoginRequest
from api.src.dependencies import get_superbet_bot_service_dependency
from api.src.services import SuperBetBotService
from api.src.settings import env

router = APIRouter()


redis_client = redis.Redis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    decode_responses=True,
)


@router.post("/schedule")
def schedule(url: str):
    # Generate a unique job ID
    job_id = str(uuid4())

    # Publish the message to Redis Stream
    redis_client.xadd(
        env.REDIS_STREAM_NAME,
        {"url": url, "job_id": job_id},
        maxlen=1000,  # Optional: Limit stream length
    )

    return {"job_id": job_id}


@router.get("/headers")
async def get_headers(
    superbet_service: Annotated[SuperBetBotService, Depends(get_superbet_bot_service_dependency)],
):
    return {"message": superbet_service.headers}


@router.post(
    "/login",
    description="Login endpoint",
)
async def login(
    item: Annotated[SuperBetLoginRequest, Body(embed=False, alias="login_data")],
    superbet_service: Annotated[SuperBetBotService, Depends(get_superbet_bot_service_dependency)],
):
    await superbet_service.start_playwright()
    try:
        return await superbet_service.get_session_and_print()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await superbet_service.stop_playwright()


@router.get(
    "/get_bets",
)
async def get_bets():
    return {"message": "Retrieved bets", "list": []}

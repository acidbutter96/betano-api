import redis
from uuid import uuid4

from typing import Annotated

from fastapi import APIRouter, Body, Depends  # , HTTPException
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
    job_id = str(uuid4())

    # Publish the message to Redis Stream
    redis_client.xadd(
        env.REDIS_STREAM_NAME,
        {
            "job_id": job_id,
            # "task_name": "default",
        },
        maxlen=1000,  # Optional: Limit stream length
    )

    return {"job_id": job_id}


@router.get(
    "/pull_active_tournaments",
)
async def push_bets():
    job_id = str(uuid4())

    # Publish the message to Redis Stream
    redis_client.xadd(
        env.REDIS_STREAM_NAME,
        {
            "job_id": job_id,
            "task_name": "pull_active_tournaments",
        },
    )

    return {"job_id": job_id}

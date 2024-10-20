from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from src.models import BetanoLoginRequest
from src.dependencies import get_betano_bot_service_dependency
from src.services import BetanoBotService
router = APIRouter()


@router.get("/headers")
async def get_headers(
    betano_service: Annotated[BetanoBotService, Depends(get_betano_bot_service_dependency)],
):
    return {"message": betano_service.headers}


@router.post(
    "/login",
    description="Login endpoint",
)
async def login(
    item: Annotated[BetanoLoginRequest, Body(embed=False, alias="login_data")],
    betano_service: Annotated[BetanoBotService, Depends(get_betano_bot_service_dependency)],
):
    await betano_service.start_playwright()
    try:
        return await betano_service.get_session_and_print()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await betano_service.stop_playwright()


@router.get(
    "/get_bets",
)
async def get_bets():
    return {"message": "Retrieved bets", "list": []}

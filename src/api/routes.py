from typing import Annotated

from fastapi import APIRouter, Body, Depends
from src.models import BetanoLoginRequest
from src.dependencies import get_undetected_chrome_driver_dependency
from undetected_chromedriver import Chrome

router = APIRouter()


@router.get("/test")
async def test(
    driver: Annotated[Chrome, Depends(get_undetected_chrome_driver_dependency)],
):
    driver.close()
    return {"message": "Hello, World!"}


@router.post(
    "/login",
    description="Login endpoint",
)
async def login(
    item: Annotated[BetanoLoginRequest, Body(embed=False, alias="login_data")]
):
    return {
        "email": item.email.email,
        "password": item.password,
    }


@router.get(
    "/get_bets",
)
async def get_bets():
    return {"message": "Retrieved bets", "list": []}

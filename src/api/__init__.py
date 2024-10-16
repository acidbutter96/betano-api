from fastapi import APIRouter
from src.api.routes import router


api_router = APIRouter()

api_router.include_router(router, prefix="/betano")

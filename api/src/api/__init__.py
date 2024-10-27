from fastapi import APIRouter
from api.src.api.routes import router


api_router = APIRouter()

api_router.include_router(router, prefix="/betano")

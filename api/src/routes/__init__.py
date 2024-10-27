from fastapi import APIRouter
from api.src.routes.routes import router


api_router = APIRouter()

api_router.include_router(router, prefix="/betano")

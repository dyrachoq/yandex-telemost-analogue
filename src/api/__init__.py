from fastapi import APIRouter

from src.api.rooms import router as rooms_router

main_router = APIRouter()

main_router .include_router(rooms_router)
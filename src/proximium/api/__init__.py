__all__ = ["api_router"]

from fastapi import APIRouter

from .user import user_router
from .auth import auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router)
api_router.include_router(auth_router)

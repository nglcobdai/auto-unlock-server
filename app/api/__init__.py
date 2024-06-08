from fastapi import APIRouter

from app.api import method

router = APIRouter()
router.include_router(method.router)

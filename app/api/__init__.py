from fastapi import APIRouter
from app.api.endpoints import method

router = APIRouter()
router.include_router(method.router)

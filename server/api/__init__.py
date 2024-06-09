from fastapi import APIRouter

from server.api import method

router = APIRouter()
router.include_router(method.router)

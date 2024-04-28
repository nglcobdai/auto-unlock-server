from fastapi import APIRouter
from app.api.endpoints import some_endpoint

router = APIRouter()
router.include_router(some_endpoint.router)

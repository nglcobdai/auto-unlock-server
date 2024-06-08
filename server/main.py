import uvicorn
from fastapi import FastAPI

from server.api import router as api_router
from server.utils.config import settings

server = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    openapi_url=settings.OPENAPI_URL,
)

server.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("server.main:server", host="0.0.0.0", port=8000, reload=True)

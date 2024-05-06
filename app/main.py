from fastapi import FastAPI
from app.api import router as api_router
from app.config import settings
import uvicorn

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    openapi_url=settings.OPENAPI_URL,
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

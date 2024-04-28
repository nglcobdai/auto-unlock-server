from fastapi import FastAPI
from app.api import router as api_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import APIRouter, BackgroundTasks, File, UploadFile

from app.src.auto_unlock import AutoUnlock
from app.utils.config import settings

ROOT_PATH = f"/api/{settings.API_VERSION}"

router = APIRouter()
auto_unlock = AutoUnlock()


@router.post(f"{ROOT_PATH}/unlock")
async def unlock(
    file: UploadFile = File(None), background_tasks: BackgroundTasks = BackgroundTasks()
):
    return await auto_unlock(file, background_tasks)

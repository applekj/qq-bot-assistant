from fastapi import APIRouter, BackgroundTasks
import uuid

from src.services import MasterService

router = APIRouter()


@router.post("/")
def chat(query: str, background_tasks: BackgroundTasks):
    master = MasterService()
    msg = master.run(query)
    uni_uid = str(uuid.uuid4())
    background_tasks.add_task(master.background_voice_synthesis, msg["output"], uni_uid)
    return {"msg": msg, "uid": uni_uid}
    # return {"msg": msg}
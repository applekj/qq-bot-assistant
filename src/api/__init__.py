from fastapi import APIRouter
from . import chat, web, ws

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(web.router, prefix="", tags=["web"])
api_router.include_router(ws.router, prefix="/ws", tags=["websocket"])
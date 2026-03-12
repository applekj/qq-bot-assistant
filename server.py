from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import api_router
from src.config import settings
import os

# 创建音频输出目录
os.makedirs(settings.audio_output_dir, exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# 挂载静态文件目录
app.mount("/audio", StaticFiles(directory=settings.audio_output_dir), name="audio")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

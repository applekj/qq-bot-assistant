from fastapi import FastAPI
from src.api import api_router
from src.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

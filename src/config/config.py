from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    # 基础配置
    app_name: str = "AI Agent API"
    debug: bool = True
    
    # OpenAI 配置
    openai_api_key: str
    openai_api_base: str
    
    # 其他 API 配置
    serpapi_api_key: str
    dashscope_api_key: str
    yuanfenju_api_key: str
    
    # 数据库配置
    redis_url: Optional[str] = None
    redis_url_local: str
    
    # Qdrant 配置
    qdrant_path: str = "./local_qdrant"
    qdrant_collection: str = "local_documents"
    
    # 音频配置
    audio_output_dir: str = "audio_output"
    
    # QQ 机器人配置
    qq_bot_token: str = ""
    qq_bot_appid: str = ""
    qq_bot_appsecret: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
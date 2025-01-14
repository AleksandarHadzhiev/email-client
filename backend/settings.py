from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str = ""
    GOOGLE_SCOPES: list = []
    GOOGLE_CLIENT_ID:str = ""
    GOOGLE_CLIENT_SECRET:str = ""
    DISCOVERY_URL:str = ""
    SECRET:str=""
    BACKEND_URL:str=""
    FRONTEND_URL:str=""
    REDIRECT_URI:str=""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf=8"
        case_sensitive = True
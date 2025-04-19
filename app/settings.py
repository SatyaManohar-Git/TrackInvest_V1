from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache
import os

env_path = Path('.')/'.env'
load_dotenv(env_path,override=True)

class Settings(BaseSettings):
    # # APP
    # APP_NAME: str = os.getenv('APP_NAME')
    # REFERER_SCRECT: str = os.getenv('REFERER_SCRECT')
    # APP_ORIGIN: str = os.getenv('APP_ORIGIN')
    # LATEST_API_VERSION: str = os.getenv('LATEST_API_VERSION')

    # # Secrets
    SECRET_KEY: str = os.getenv('SECRET_KEY') 
    ALGORITHM: str = os.getenv('ALGORITHM') 
    username: str = os.getenv('username') 
    password: str = os.getenv('password') 

    # ACCESS_TOKEN_EXPIRE_MINUTES:int = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    # REFRESH_TOKEN_EXPIRE_MINUTES:int = timedelta(minutes=int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')))
    # ALGORITHM: str = os.getenv('ALGORITHM')

    # # Database
    # SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')
    # DB_CREATE_ALL : bool = bool(os.getenv('DB_CREATE_ALL'))

@lru_cache
def get_settings() -> Settings:
    return Settings()


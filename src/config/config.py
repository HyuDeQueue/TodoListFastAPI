import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str
    DATABASE_URL: str
    JWT_EXPIRATION: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

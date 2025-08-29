import os
from dotenv import load_dotenv # Убедись, что добавил python-dotenv в requirements

load_dotenv()

class Settings:
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "3306")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "esport_platform")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "root") 
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "") 
    SECRET_KEY: str = os.getenv("SECRET_KEY", "") 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
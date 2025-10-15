from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Use SQLite by default for easy development (no PostgreSQL needed)
    # Change to PostgreSQL URL for production
    DATABASE_URL: str = "sqlite:///./strumind.db"
    
    # For PostgreSQL, use:
    # DATABASE_URL: str = "postgresql://strumind_user:strumind_pass@localhost:5432/strumind"
    
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

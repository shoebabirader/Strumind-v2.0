from pydantic_settings import BaseSettings
import os
import secrets

class Settings(BaseSettings):
    # SECURITY FIX: No hardcoded credentials - use environment variables
    # Database configuration from environment
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./strumind.db"  # Safe default for development only
    )
    
    # SECURITY FIX: Generate secure secret key from environment
    # CRITICAL: Set JWT_SECRET environment variable in production!
    JWT_SECRET: str = os.getenv(
        "JWT_SECRET",
        secrets.token_urlsafe(32) if os.getenv("ENVIRONMENT") == "development" else None
    )
    
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Environment indicator
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Security settings
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "*").split(",")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate critical security settings in production
        if self.ENVIRONMENT == "production":
            if not self.JWT_SECRET or self.JWT_SECRET == "your-secret-key-change-in-production":
                raise ValueError(
                    "CRITICAL SECURITY ERROR: JWT_SECRET must be set in production environment! "
                    "Set the JWT_SECRET environment variable with a secure random value."
                )
            if self.DATABASE_URL == "sqlite:///./strumind.db":
                raise ValueError(
                    "CRITICAL: SQLite should not be used in production! "
                    "Set DATABASE_URL environment variable to a production database."
                )

settings = Settings()

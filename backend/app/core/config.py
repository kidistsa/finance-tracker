from typing import List, Optional, Union, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator, Field
import secrets
import json
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Personal Finance Tracker API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Backend API for Personal Finance Tracker"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    API_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Fixed parsing
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
   

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"
    FIREBASE_STORAGE_BUCKET: str = ""
    FIREBASE_PROJECT_ID: str = ""
    
    # Plaid (Open Banking)
    PLAID_CLIENT_ID: str = ""
    PLAID_SECRET: str = ""
    PLAID_ENV: str = "sandbox"
    PLAID_WEBHOOK_URL: Optional[str] = None
    
    # Database
    DATABASE_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = [".csv"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                # Try to parse as JSON
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    # If JSON parsing fails, split by comma
                    return [origin.strip() for origin in v.strip("[]").split(",") if origin.strip()]
            else:
                # Split by comma
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse allowed extensions"""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    return [ext.strip() for ext in v.strip("[]").split(",") if ext.strip()]
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v


settings = Settings()
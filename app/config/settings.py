import os
from pydantic import BaseSettings

from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    API_KEY: str = os.getenv("API_KEY")
    PROJECT_NAME: str = 'notification-service-v2'

    SMTP_PORT: int = 465
    SMTP_SERVER: str = "smtp.gmail.com"
    EMAIL_FOR_SENDING: str = "ddc.dev.python@gmail.com"
    EMAIL_LOGIN: str = "ddc.dev.python@gmail.com"
    EMAIL_PASSWRD: str = os.getenv('EMAIL_PASSWRD')

    CELERY_BROKER_URL: str ="redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str ="redis://redis:6379/0"

    LOG_DIRECTORY: str = "./logs" # Always put the log directory in the CWD.
    LOG_ARCHIVE_DIRECTORY: str = f"{LOG_DIRECTORY}/log-archives"
    DEFAULT_LOG_FILE: str = f"{LOG_DIRECTORY}/DEFAULT-app-logs.log"  # This where all log entries go If a destnation is not specified.
    ALGORITHM: str = "HS256"
    
    # Only let the Auth API connect for now.
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:8015'] # development

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
settings = Settings()
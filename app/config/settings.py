import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = os.getenv("API_KEY")
    PROJECT_NAME: str = 'email-service-v2'
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

settings = Settings()
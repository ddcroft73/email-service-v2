from os import getenv
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = getenv("API_KEY")
    SMTP_PORT: int = 465
    SMTP_SERVER: str = "smtp.gmail.com"
    EMAIL_FOR_SENDING: str = "ddc.dev.python@gmail.com"
    EMAIL_LOGIN: str = "ddc.dev.python@gmail.com"
    EMAIL_PASSWRD: str = getenv('EMAIL_PASSWRD')

    CELERY_BROKER_URL: str ="redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str ="redis://redis:6379/0"

    LOGFILE_INFO: str = ''
    LOGFILE_ERROR: str= ''

    
settings = Settings()
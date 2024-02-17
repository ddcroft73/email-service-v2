
from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import Optional, Union
from app.config.settings import settings 

class Email(BaseModel):
    email_to: EmailStr
    email_from: EmailStr
    subject: str
    message: str     
    user_id: Optional[str] = None


class MailResponse(BaseModel):
    result: str

class BasicResponse(BaseModel):
    result: Union[str, int, dict]    

class TextMessage(BaseModel):
    text_to: str  # THe actual address to send to will be built later
    text_from: str = settings.EMAIL_FOR_SENDING
    message: str
    user_id: Union[str, int, None] = None
    

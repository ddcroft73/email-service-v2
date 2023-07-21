from pydantic import BaseModel
from typing import Optional

class UserInfo(BaseModel):
    userid: str
    user_uuid: str
    account_type: str

class Message(BaseModel):
    text: str 
    html: str
    
class Email(BaseModel):
    email_to: str
    email_from: str
    subject: str
    message: Message    
    users_info: Optional[UserInfo] = None


class MailResponse(BaseModel):
    result: str

class BasicResponse(BaseModel):
    result: str    
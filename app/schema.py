from pydantic import BaseModel
from typing import Optional

class UserInfo(BaseModel):
    userid: str
    passwrd: str
    user_uuid: str

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
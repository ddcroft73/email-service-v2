from pydantic import BaseModel
from typing import Optional
   
class Email(BaseModel):
    email_to: str
    email_from: str
    subject: str
    message: str     
    user_id: Optional[str] = None


class MailResponse(BaseModel):
    result: str

class BasicResponse(BaseModel):
    result: str    
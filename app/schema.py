from pydantic import BaseModel

class Message(BaseModel):
    text: str 
    html: str 

class Email(BaseModel):
    email_to: str
    email_from: str
    subject: str
    message: Message

class MailResponse(BaseModel):
    result: str
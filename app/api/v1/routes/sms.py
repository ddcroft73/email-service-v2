
from fastapi import APIRouter, Depends, status
from app.api.schema.schema import Email, MailResponse
router = APIRouter()

@router.post('/send-sms/', 
    response_model=MailResponse, 
    status_code=status.HTTP_201_CREATED
)
def send_sms():
    pass
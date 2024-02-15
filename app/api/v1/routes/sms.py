
from fastapi import APIRouter, Depends, status
from app.api import schema 
from app.utils.utils import verify_token, send_text_message_via_email
from typing import Any

from app.utils.logger import logzz


router = APIRouter()

@router.post('/send-email-sms/', 
    response_model=schema.MailResponse, 
    status_code=status.HTTP_201_CREATED
)
async def send_email_sms(
    text_message: str,
    provider: str,
    payload: dict=Depends(verify_token)
) -> Any:
    '''
      Leverages The email sednng code to dens a text message va the EMail gateway.
      Al you need is the users provider and cell number. Formatted like so:
      5551234567@provider.com And you have 100% free text messages sent to your users.

      SHould crreate a dedicated email address for this... SMS.Delvery@yourapp.net
    '''
    response: bool = await send_text_message_via_email(text_message, provider) 
    logzz.info(f"SMS Text Sent to: {text_message.text_to}.", timestamp=1)

    return {"result": response} 


from fastapi import APIRouter, Depends, status
from app.api import schema 
from app.utils.utils import verify_token, send_text_message_via_email, PROVIDERS

from typing import Any, Union

from app.utils.logger import logzz


router = APIRouter()


@router.post('/send-email-sms/',  response_model=schema.BasicResponse,  status_code=status.HTTP_201_CREATED)
async def send_email_sms(
    _message: str,
    _phone_number: str,
    _provider: str,
    _user_id: Union[str, int],
    payload: dict=Depends(verify_token),
) -> Any:
    '''
      Leverages your smtp email service to send a text message. Need the phone #, and service provider.
    '''    
    message_gateway: str = "mms"

    if (not PROVIDERS.get(_provider).get('mms_support')):
        message_gateway = "sms" 
           
    #If the mms gateway and sms are the same, default to the mms gateway.
    receiver_email: str = f'{_phone_number}@{PROVIDERS.get(_provider).get(message_gateway, PROVIDERS.get(_provider).get("mms"))}'
    
    text_message = schema.TextMessage(
         text_to=receiver_email,
         message=_message,
         user_id=_user_id
    )
    
    response: str = await send_text_message_via_email(text_message) 

    logzz.info(f"MMS Text Sent to: {text_message.text_to}.", timestamp=1)

    return {"result": response} 

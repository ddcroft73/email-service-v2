
from fastapi import APIRouter, Depends, status, Body,HTTPException
from app.api import schema 
from app.utils.utils import verify_token, send_text_message_via_email, PROVIDERS
from typing import Any, Union
from app.utils.logger import logzz


router = APIRouter()


@router.post('/send-email-sms/',  response_model=schema.BasicResponse,  status_code=status.HTTP_201_CREATED)
async def send_email_sms(
    message: str = Body(...),
    phone_number: str = Body(...),
    provider: str = Body(...),
    user_id: Union[str, int, None] = Body(...),
    payload: dict=Depends(verify_token),
) -> Any:
    '''
      Leverages your smtp email service to send a text message. Need the phone #, and service provider.
    '''    
    message_gateway: str = "mms"

    if (not PROVIDERS.get(provider).get('mms_support')):
        message_gateway = "sms" 
           
    # If the mms gateway and sms are the same, default to the mms gateway.
    # MMS just seems to be more trust worthy. SMS likes to split messages into pieces, and thats
    # not 
    receiver_text_address: str = f'{phone_number}@{PROVIDERS.get(provider).get(message_gateway, PROVIDERS.get(provider).get("mms"))}'
    
    text_message = schema.TextMessage(
         text_to=receiver_text_address,
         message=message,
         user_id=user_id
    )    

    response: str = await send_text_message_via_email(text_message) 
    if not response:
        raise HTTPException(
            status_code=400, 
            detail="SMTP Error sending email for text mesage"
        )
    
    return {"result": response} 

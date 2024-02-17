from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from app.core.settings import settings
from app.api.schema.schema import Email, TextMessage
from .providers import PROVIDERS
from .smtp_email import smtp_email
from .logger import logzz 
from typing import Union, Any


async def dispatch_email(email: Email) -> str:    
    response:  Union[bool, str] = await smtp_email.send_async(email)    

    if response == True:
        logzz.info(
            f"Email  dispatched to: {email.email_to} ", 
            timestamp=True
        )        
        return f"Email sent @ {logzz.d_and_t.date_time_now()}"
    
    else:
        logzz.error(f" func: 'dispatch_email()' Error after 'smtp_email.send_async()\n{response}' ")
       
        return response
    
    



async def send_text_message_via_email(tm: TextMessage) -> str:
    response: Union[bool, str] = await smtp_email.send_text_message(tm)    

    if response == True: # Must be explict, since response can be boolean or str. str would also be truthy, and cause a false positive.

        logzz.info(
            f"Text Messsage dispatched to: {tm.text_to} ", 
            timestamp=True
        )

        return f"Text sent @ {logzz.d_and_t.date_time_now()}"
    else:
        logzz.error(
            f" func: 'send_text_message_via_email()' {response}' "
        )
        return response
    
    


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict:
    '''
    THis service was built to be a part of a micro service architecture and as such,
    requires a token created in the auth service to be used. 
    The security is implemented via dependecy injection in the endpoints and to disable it
    just delete that parameter.
    '''
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.API_KEY, algorithms=["HS256"])
        return payload

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


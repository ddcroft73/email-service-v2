from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from app.config.settings import settings
from app.api.schema.schema import Email, TextMessage
from .providers import PROVIDERS
from .smtp_email import smtp_email
from .logger import logzz 


async def dispatch_email(email: Email) -> str:    
    response: bool = await smtp_email.send_async(email)    
    if response:
        logzz.info(
            f"Email  dispatched to: {email.email_to} ", 
            timestamp=True
        )
    else:
        logzz.error(" func: 'dispatch_email()' Error after 'smtp_email.send_async()' ")
        raise HTTPException(
            status_code=400, 
            detail="SMTP Error"
        )
    
    # message back to client success
    return f"email sent @ {logzz.d_and_t.date_time_now()}"



async def send_text_message_via_email(tm: TextMessage) -> str:
    response: bool = await smtp_email.send_text_message(tm)    
    if response:
        logzz.info(
            f"Text Messsage dispatched to: {tm.text_to} ", 
            timestamp=True
        )
    else:
        logzz.error(" func: 'send_text_message_via_email()' Error after 'smtp_email.send_mms_text(tm)' ")
        raise HTTPException(
            status_code=400, 
            detail="SMTP Error Sending Email for Text mesage"
        )
    
    # message back to client        
    return f"Text sent @ {logzz.d_and_t.date_time_now()}"


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


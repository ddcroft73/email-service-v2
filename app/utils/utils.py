from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from app.config.settings import settings
from app.api.schema.schema import Email
from .smtp_email import smtp_email
from .logger import logzz 


async def dispatch_email(email: Email) -> dict:    
    response = await smtp_email.send_async(email)    
    if response:
        print("sending mail...")
    else:
        logzz.error(" func: 'dispatch_email()' Error after 'smtp_email.send_async()' ")
        raise HTTPException(status_code=400, detail="SMTP Error")
    
    # back to client        
    return f"email sent @ {logzz.d_and_t.date_time_now()}"


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict:
    try:
        token = credentials.credentials

        payload = jwt.decode(token, settings.API_KEY, algorithms=["HS256"])
        return payload

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


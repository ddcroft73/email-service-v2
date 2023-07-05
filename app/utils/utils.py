
from fastapi import ( 
    Depends, 
    HTTPException, 
    status
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from fastapi.responses import JSONResponse
import jwt, os
from jwt.exceptions import PyJWTError
from config.settings import settings
from schema import Email
from .smtp_email import smtp_email
from datetime import datetime, timedelta


async def dispatch_email(email: Email) -> dict:

    response = await smtp_email.send_mail(email)   
    #sleep(3)     
    if response:
       print("sending mail...")
    else:
       
       return {'inner result': 'Something went wrong.'}
    # back to client   
    return {'inner result': f"email sent @ {datetime.now()}"}  



def verify_token(credentials: HTTPAuthorizationCredentials=Depends(HTTPBearer())) -> dict:
    try:
        token = credentials.credentials

        payload = jwt.decode(token, settings.API_KEY, algorithms=["HS256"])
        return payload
    
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    


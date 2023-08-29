'''

The main routes:

 send_mail/
 send_async/
'''
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.api.schema.schema import Email, MailResponse
from app.utils.utils import (
    verify_token,
    dispatch_email
)    
from app.worker import send_email_task
from app.utils.logger import logzz
router = APIRouter()

@router.post('/send-email/', 
    response_model=MailResponse, 
    status_code=status.HTTP_201_CREATED
)
def send_email(
    email: Email,  payload: dict=Depends(verify_token)
):      
    task =  send_email_task.delay(email.dict())      
    response = {        
       "result": f'{task.id}, Task passed to Celery'
    }
    logzz.info(f"Email Sent to: {email.email_to}", timestamp=1)
    return JSONResponse(response)    
 

@router.post('/send-async/', 
    response_model=MailResponse, 
    status_code=status.HTTP_201_CREATED
)
async def send_async(
    email: Email, payload: dict=Depends(verify_token) 
):
    response: bool = await dispatch_email(email) 
    return JSONResponse({"result": response})    


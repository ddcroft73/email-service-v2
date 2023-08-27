'''

The main routes:

 send_mail/
 send_async/
'''
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.api.schema.schema import Email, MailResponse, BasicResponse
from app.utils.utils import (
    verify_token,
    dispatch_email
)    
from app.utils.smtp_email import smtp_email
from app.utils.logger import logzz
from app.utils.file_handler import filesys
from app.config.settings import settings
from app.worker import send_email_task
import os

router = APIRouter()

@router.post('/send-email/', 
    response_model=MailResponse, 
    status_code=status.HTTP_201_CREATED
)
def send_email(
    email: Email,  payload: dict=Depends(verify_token)
):      
    task =  send_email_task.delay(email.dict())         
     #response = await dispatch_email(email) #without Celery. it still works just add async \await down the chain. 
    response = {        
       "result": f'{task.id}, Task passed to Celery'
    }
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


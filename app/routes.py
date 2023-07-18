from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schema import Email, MailResponse
from utils.utils import verify_token, dispatch_email
from utils.smtp_email import smtp_email
from worker import send_email_task
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get('/', 
    response_class=RedirectResponse
)  
def index():
    return RedirectResponse(url='/static/index.html')

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




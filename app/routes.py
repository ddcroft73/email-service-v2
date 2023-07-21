from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schema import Email, MailResponse, BasicResponse
from utils.utils import verify_token, dispatch_email
from utils.smtp_email import smtp_email
from utils.logger import logzz
from utils.file_handler import filesys
from config.settings import settings
from worker import send_email_task
from fastapi.responses import RedirectResponse
import os

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


@router.post('/manage-archive/{command}', 
    response_model=BasicResponse,
    status_code=201
)
def manage_archive(command: str, payload: dict=Depends(verify_token)) -> None:
    '''
    command = either the dir to delete, --all for all, or other(TBD)

    looking for:
      1. The name of an archive directory, or directories. 
      2. The flag: --all
    
    If a directory with the name <dir> exists, it will be cleared.
    If <dir> == --all, then they will all be cleared. 
    
    THIS CODE IS NOT PERMENANT. JUST CONCIEVING IDEAS... 
    '''
    user_choice_exists: bool = filesys.exists(os.path.join(settings.LOG_ARCHIVE_DIRECTORY, command))
    status: str = "The archive directories have been deleted. "
    try:
        #filesys.rmdir(settings.LOG_ARCHIVE_DIRECTORY)
        #logzz.info("Success deleting the archive directories.", timestamp=True) 
        if user_choice_exists:
            logzz.info(f'dir: {command} Exists.')
            status = f'{command} does indeed, exist.'
        elif command == '--all' and not user_choice_exists:
            logzz.info(f'dir: {command} --all.')
            status = f'{command} All will be cleared.'

        
    except Exception as exc:
        print("ERROR: Error deleting the archive directory.")
        status = "ERROR: Error deleting the archive directory."
        logzz.error("Could not delete the archive directories...")


    return JSONResponse( {'result': f'Authorized. Status: {status}'})
    




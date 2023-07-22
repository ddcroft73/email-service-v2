from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schema import Email, MailResponse, BasicResponse
from utils.utils import (
    verify_token,
    dispatch_email
)    
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
    status_code=status.HTTP_200_OK
)
def manage_archive(command: str, payload: dict=Depends(verify_token)) -> None:
    '''
    command = either the command to delete, --all for all, or --wipe to start at ./logs and obliterate

    looking for:
      1. The name of an archive directory. 
      2. The flag: --all, --wipe
    
    If a directory with the name <command> exists, it will be cleared.
    If <command> == --all, then they will all be cleared. but remain intact
    If <command> == --wipe, All logs are wiped and not rebuilt
     
    Lawd have mercy.... this is NOT my finest code... But it do be working, so theres that. 
    will refactor... 
    '''
    
    subs: list[str] = 'info,error,debug,warn'.split(',')
    status: str = f'{settings.LOG_ARCHIVE_DIRECTORY}/{command+"/" if command in subs else ""}  clear success. command: {command}'
    cleared: str = 'done'

    try:
       if command == '--all':                          # All the sub directories
           logzz.archive.clear_subs(subs)

       elif command == "--wipe":                       # Fuck it, nuke em from ./logs on down. 
          filesys.rmdir(settings.LOG_DIRECTORY)
          status = f'Totally wiped: {settings.LOG_DIRECTORY}'
          cleared = 'wiped'     

       elif command in subs:
           logzz.archive.clear_subs([command])
       else:
           cleared = 'nope'                            # Do nada cause some stupid nonsensical command got through. 
           status = f'{settings.LOG_ARCHIVE_DIRECTORY} remains untouched.'
           
       # How to notify of results:
       if cleared == 'done':
            logzz.info(
                f"Cleared: {settings.LOG_ARCHIVE_DIRECTORY}/{command+'/' if command in subs else ''}\n"
                f"{logzz.INFO_PRE}The command was: {command}"
            ) 
       elif cleared == 'wiped':
           logzz.info(
                f"Totally wiped: {settings.LOG_DIRECTORY}\n"
                f"{logzz.INFO_PRE}The command was: {command}"
            )       
       elif cleared == 'nope':
           logzz.info(
                f"No clearing took place in: {settings.LOG_ARCHIVE_DIRECTORY}\n"
                f"{logzz.INFO_PRE}The command was: {command}"
            )     
       
           
    except Exception as exc:
        print("ERROR: Error deleting the archive directory.")
        status = "ERROR: Error deleting the archive directory."
        logzz.error(f"Could not delete the archive directories... Exc: {str(exc)}")

    return JSONResponse( {'result': f'Status: {status}'})
    

@router.get('/export-all-archives/', 
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK
)
def export_all_archives(payload: dict=Depends(verify_token)) -> None:
    '''
    This endpoint will facilitate the zip archiving of all the files in ./logs
    Once they are zipped... the download link will be returned to the client.
    The client has the option to delete the .zip file on download. 

    '''
    status: str= 'Testing...'
    return JSONResponse( {'result': f'Status: {status}'})


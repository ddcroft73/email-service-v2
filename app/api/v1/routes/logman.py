'''
Routes to manage the logs in the api. 

manage_archive/{command}/
export_all_archives/
'''
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.api.schema.schema import BasicResponse
from app.utils.utils import verify_token    
from app.utils.logger import logzz
from app.utils.file_handler import filesys
from app.config.settings import settings
import os, time
router = APIRouter()


@router.post('/manage-archive/{command}', 
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK
)
def manage_archive(command: str, payload: dict=Depends(verify_token)) -> None:
    '''    
    command:
      This can be a single log file name, or multiple seperated by a comma.
      a single archived directory or string of directories.
      --all for all directories
      --wipe for the entire log directory. 
    The files will be recreated and archive dirs as well.  

    This is still using an older version of APILogger
    '''
    
    subs: list[str] = 'info,error,debug,warn'.split(',')
    status: str = f'{settings.LOG_ARCHIVE_DIRECTORY}/{command+"/" if command in subs else ""}  clear success. command: {command}'
    cleared: str = 'done'
    
    # if the user entered a comma delimted list then they want to dispose of more than 
    # one file, or srchive directory
    if command.find(',') != -1:
        command = command.split(',')

    try:
       if command == '--all':                          # All the sub directories
           logzz.archive.clear_subs(subs)

       elif command == "--wipe":                       # Fuck it, nuke em from ./logs on down. 
          filesys.rmdir(settings.LOG_DIRECTORY)
          status = f'Totally wiped: {settings.LOG_DIRECTORY}'
          cleared = 'wiped'     

       elif command in subs and isinstance(command, str):
           logzz.archive.clear_subs([command])

       elif isinstance(command, list) :
           # loop over list and see if each item is a file or directory
           # if its a file, delete it, if its a directory, remove it.
           status = f'Removed multiple items: {command}'
           for item in command:
               if item in subs:
                   #dir
                   path = os.path.join(settings.LOG_ARCHIVE_DIRECTORY, item)
                   filesys.rmdir(path)
                   logzz.info( f"Remove Directory: {path}")
                   filesys.mkdir(path)
                   logzz.info( f"Remake Directory: {path}")
               else:
                   #file 
                   path = os.path.join(settings.LOG_DIRECTORY, item)
                   filesys.delete(path)              
                   logzz.create_logfile(path)           
                   logzz.info( f"Delete File: {path}")        
                   logzz.info(f"File remade: {path}")

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
           # Need to respawn the directories so logs will work
           logzz.setup()           
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


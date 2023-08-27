import os, sys, time, requests, asyncio, aiohttp
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
# import cant find the files if you start a file from inside the directory structure.
cwd = os.getcwd()
sys.path.append(cwd)

from schema import Email, Message
from utils.utils import create_token
from test_html_template import html 
from settings import settings 


# THis script has to be ran from another project.

email = Email(
    email_to="croftdanny1973@gmail.com",
    email_from=settings.EMAIL_FOR_SENDING,
    subject="Test Email",
    message=html,
    user_id= None
)    


load_dotenv()

def test_obliterate_archive_directories(token: str, dir: str):
    url = f'http://0.0.0.0:8014/api/manage-archive/{dir}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    tag: str = 'testing... testing'
    

    response = requests.request(
        "POST", 
        url, 
        headers=headers
    )

    print(response.json())



def test_email(token: str, endpoint: str):
    url = f'http://0.0.0.0:8014/api/{endpoint}/'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    #for _ in range(1):
    ##    time.sleep(1)
    
    response = requests.request(
            "POST", 
            url, 
            headers=headers, 
            json=email.dict()
        )

    print(response.json())


async def test_root():
    url = 'http://localhost:8014/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def call_test():
    res = await test_root()
    print(res)

#asyncio.run(call_test())



token:  str = create_token()#'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlRlc3R0aGVTZXJ2aWNlIiwiZXhwIjoxNjg5NzE3NTAyLCJpc3MiOiJ5b3VyLWlzc3VlciIsInN1YiI6InVzZXItMTIzNDUifQ.TQayrNEqP_ONVXgltCuydruNjywlnPKw0E6mSr7YtP4'
#print(token)
endpoint: str = 'send-email'
test_email(token, endpoint)
#test_obliterate_archive_directories(token, dir="debug")

import os, sys, requests
sys.dont_write_bytecode = True

# So I can import the files i need to test
cwd = os.getcwd()
sys.path.append(cwd)

from app.api.schema.schema import Email
from test_html_template import html 
from app.config.settings import settings 
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

def create_token() -> str:
    return jwt.encode({"test": "data"}, settings.API_KEY, algorithm=settings.ALGORITHM)


# To delete the archives on the server, I have since deleted the endpoints but may add them again.
def test_obliterate_archive_directories(token: str, dir: str):
    url = f'http://0.0.0.0:8014/api/v1/logs/manage-archive/{dir}'

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
    url = f'http://0.0.0.0:8014/api/v1/mail/{endpoint}/'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # WHen testing make sure you have access to an SMTP service. 
    # devnoted by email_from
    email = Email(
        email_to="youremail@email.com",
        email_from="SMTP_service@mail.com",
        subject="EMAIL TESTING",
        message=html,
        user_id= None
    )    
    
    #for _ in range(1):
    ##    time.sleep(1)    
    response = requests.request(
            "POST", 
            url, 
            headers=headers, 
            json=email.dict()
        )

    print(response.json())



#asyncio.run(call_test())



token:  str = create_token()

endpoint: str = 'send-email'
test_email(token, endpoint)
#test_obliterate_archive_directories(token, dir="debug")

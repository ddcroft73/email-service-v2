import os, sys, time, requests
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
# import cant find the files if you start a file from inside the directory structure.
cwd = os.getcwd()
sys.path.append(cwd)

from app.schema import Email, Message
from app.utils.utils import create_token
from test_html_template import html 
from app.config.settings import settings 


# An email mustbe setup like so before itis dispatched to the service. It wiull be validated on the client... in JS, YEH, effing JAVASCRIPT.
# Killme now.

email = Email(
    email_to="croftdanny1973@gmail.com",
    email_from=settings.EMAIL_FOR_SENDING,
    subject="Test Email",
    message=Message(
        text="This is a test Email, THe Text Plain Text Portion",
        html=html
    )    
)

load_dotenv()

def test_email(token):
    url = 'http://localhost:8014/send-email/'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    for _ in range(1):
        time.sleep(1)

        response = requests.request(
            "POST", 
            url, headers=headers, 
            json=email.dict()
        )

        print(response.json())




token:  str = create_token() #'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlRlc3R0aGVTZXJ2aWNlIiwiZXhwIjoxNjg4MjU0NjUwLCJpc3MiOiJ5b3VyLWlzc3VlciIsInN1YiI6InVzZXItMTIzNDUifQ.8bZgW0xObI7HePQkbeMqVktjSsioHdicKM8u72sCatY' #reate_token()
print(token)
test_email(token)
# I'm currently learning how to launch tests from within the container. My testing till now has consisted
# of a loop firing as many requests as I want at the endpoint, and making the taskstake random amounts of time.
# This little service can take it. The creator of fastAPI and creators of Celery have been teaching me a lot.

# This is a standalone script that should be ran in another containre or in its own venv. I tested it by runing
# this script from inside V1.

import os, sys, time, requests, asyncio, aiohttp
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
        text="This is a test Email, THe Text Plain Text Portion", html=html
    ),
)

load_dotenv()


def test_email(token):
    url = "http://0.0.0.0:8014/send-email/"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # for _ in range(1):
    ##    time.sleep(1)

    response = requests.request("POST", url, headers=headers, json=email.dict())

    print(response.json())


async def test_root():
    url = "http://localhost:8014/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def call_test():
    res = await test_root()
    print(res)


# asyncio.run(call_test())


token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlRlc3R0aGVTZXJ2aWNlIiwiZXhwIjoxNjg5MTA3NDg0LCJpc3MiOiJ5b3VyLWlzc3VlciIsInN1YiI6InVzZXItMTIzNDUifQ.Pm9jJ_g0L6pMtYLDbDnSuSK0wQ3hyT3O-IskBZ0Gd7g"  # create_token()
# print(token)
test_email(token)

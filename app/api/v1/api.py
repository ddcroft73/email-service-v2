'''
From here you reach out to files where the rout3es live. 
'''

from fastapi import APIRouter 
from .routes.mail import router as mail_router
from.routes.logman import router as log_router

api_router = APIRouter()

api_router.include_router(
    mail_router,
    prefix='/mail',
    tags=['mail']
)

api_router.include_router(
    log_router,
    prefix='/logs',
    tags=['logs']
)
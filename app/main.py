from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.utils.logger import logzz

app = FastAPI()

app.mount("/app/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(router, prefix="/api")

#logzz.error("Aint no error. I just want to see it log.", timestamp=True)/
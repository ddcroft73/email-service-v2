from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
from utils.logger import logzz

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

#logzz.error("Aint no error. I just want to see it log.", timestamp=True)
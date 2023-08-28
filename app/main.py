from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.api.v1.api import api_router
from app.utils.logger import logzz
from app.config.settings import settings

app = FastAPI()

app.mount(
    "/app/static", 
    StaticFiles(directory="./app/static"), 
    name="static"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def main():
     return RedirectResponse(url="/app/static/index.html", status_code=HTTP_302_FOUND)

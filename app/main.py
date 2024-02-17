from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.api.v1.api import api_router
from app.utils.logger import logzz
from app.core.settings import settings

app = FastAPI()

app.mount(
    "/app/static", 
    StaticFiles(directory="./app/static"), 
    name="static"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def main():
     return RedirectResponse(url="/app/static/index.html", status_code=HTTP_302_FOUND)

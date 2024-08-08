from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .auth.views import router as auth_router
from .dashboard.views import router as dashboard_router

app = FastAPI()

app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(auth_router, prefix="/auth")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware)

from fastapi import APIRouter

from .home import router as home_router

routes = APIRouter()

routes.include_router(home_router, tags=["home"])
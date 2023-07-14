from asgi_htmx import HtmxRequest as Request
from fastapi import APIRouter
from jinja2_fragments.fastapi import Jinja2Blocks

from app.core.config import Settings

settings = Settings()

router = APIRouter()

template = Jinja2Blocks(settings.TEMPLATE_DIR)


@router.get("/")
def homepage(request: Request):
    return template.TemplateResponse(
        "main.html",
        context = {
            "request": request,
            "site_name": "PyHAT Skeleton",
            "page_title": "Build a PyHAT site!",
        }
        )
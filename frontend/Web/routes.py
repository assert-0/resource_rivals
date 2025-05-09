from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from settings import env

api_router = APIRouter(prefix="")
templates = Jinja2Templates(directory="static/templates/")


@api_router.get("/index")
@api_router.get("/index.html")
@api_router.get("/")
async def get_index(request: Request):
    """
    This is the index route.
    """

    return templates.TemplateResponse(
        name="index.html.jinja2",
        request=request,
        context={
            "env": env.dump(),
        },
    )


@api_router.get("/game")
@api_router.get("/game.html")
def get_game(request: Request):
    """
    This is the game route.
    """
    return templates.TemplateResponse(
        name="game.html.jinja2",
        request=request,
        context={
            "env": env.dump(),
        },
    )


@api_router.get("/favicon.ico")
async def get_favicon(request: Request):
    """
    This is the favicon route.
    """
    return RedirectResponse(
        url="static/icons/favicon.ico",
        status_code=302,
    )

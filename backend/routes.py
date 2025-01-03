import typing
from typing import List, Union

from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import JSONResponse

api_router = APIRouter()


@api_router.get("/")
async def placeholder() -> JSONResponse:
    return JSONResponse(content={"hello": "world"})

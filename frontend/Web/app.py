import sys

sys.path.append(__file__.rsplit("/", 1)[0])
sys.path.append(__file__.rsplit("\\", 1)[0])

from fastapi import FastAPI  # noqa: E402
from starlette.staticfiles import StaticFiles  # noqa: E402

from routes import api_router  # noqa: E402


app = FastAPI()
app.include_router(api_router)

app.mount(
    "/static",
    StaticFiles(directory="static/"),
    name="static",
)

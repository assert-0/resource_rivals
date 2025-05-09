import sys

sys.path.append(__file__.rsplit("/", 1)[0])
sys.path.append(__file__.rsplit("\\", 1)[0])

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from routes import api_router  # noqa: E402
from settings import ALLOWED_ORIGINS  # noqa: E402


app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

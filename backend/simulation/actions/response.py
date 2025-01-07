from pydantic import BaseModel


class Response(BaseModel):
    error: str = ""

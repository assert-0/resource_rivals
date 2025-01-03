from abc import ABC
from uuid import uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel, ABC):
    id: str = Field(default_factory=lambda: str(uuid4()))
    x: int
    y: int
    type: str

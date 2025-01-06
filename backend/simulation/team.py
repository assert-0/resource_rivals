from typing import Set
from uuid import uuid4

from pydantic import BaseModel, Field

from utils.math import Point


class Resources(BaseModel):
    food: int = 0
    wood: int = 0
    minerals: int = 0


class Team(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    visibleArea: Set[Point] = Field(default_factory=set)
    resources: Resources = Resources()

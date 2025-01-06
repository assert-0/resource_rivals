from typing import List

from pydantic import Field, BaseModel

from simulation.actions.action import Action
from simulation.map import Map


class History(BaseModel):
    actions: List[Action] = Field(default_factory=list)
    mapStates: List[Map] = Field(default_factory=list)

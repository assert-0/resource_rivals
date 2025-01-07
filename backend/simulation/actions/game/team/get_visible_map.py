from typing import List, Optional

from pydantic import BaseModel

from entities.entity import Entity
from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.team_action import TeamAction


class GetVisibleMapRequest(TeamAction, ConcreteAction):
    pass


class GetVisibleMapResponse(BaseModel):
    sectors: List[List[Optional[List[Entity]]]]

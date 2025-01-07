from typing import List

from pydantic import BaseModel

from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.unit.move.move_action import MoveAction
from utils.math import Point


class GetReachableSectorsRequest(MoveAction, ConcreteAction):
    pass


class GetReachableSectorsResponse(BaseModel):
    sectors: List[Point]

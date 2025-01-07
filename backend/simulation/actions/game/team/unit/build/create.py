from pydantic import BaseModel

from entities.entity import Entity
from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.unit.build.build_action import BuildAction


class CreateRequest(BuildAction, ConcreteAction):
    buildingType: str
    buildingNamespace: str


class CreateResponse(BaseModel):
    building: Entity

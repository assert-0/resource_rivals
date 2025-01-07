from typing import List

from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.unit.build.build_action import BuildAction
from simulation.actions.response import Response


class GetAvailableBuildingsRequest(BuildAction, ConcreteAction):
    pass


class GetAvailableBuildingsResponse(Response):
    availableBuildings: List[List[str]]  # (namespace, type) tuples

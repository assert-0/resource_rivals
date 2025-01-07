from typing import List

from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.unit.build.build_action import BuildAction


class GetAvailableBuildingsRequest(BuildAction, ConcreteAction):
    pass


class GetAvailableBuildingsResponse(BuildAction, ConcreteAction):
    availableBuildings: List[List[str]]  # (namespace, type) tuples

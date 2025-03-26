from entities.dynamic.units.unit import UnitMoveResult
from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.unit.move.move_action import MoveAction
from simulation.actions.response import Response

from utils.math import Point


class CreateRequest(MoveAction, ConcreteAction):
    targetPosition: Point


class CreateResponse(Response, UnitMoveResult):
    pass

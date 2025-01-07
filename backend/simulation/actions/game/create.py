from pydantic import BaseModel

from simulation.actions.action import ConcreteAction
from simulation.actions.game.game_action import GameAction
from simulation.game import Game


class CreateRequest(GameAction, ConcreteAction):
    mapName: str


class CreateResponse(BaseModel):
    game: Game

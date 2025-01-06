from pydantic import BaseModel

from simulation.actions.action import ConcreteAction
from simulation.actions.game.game_action import GameAction
from simulation.game import Game


class ReadRequest(GameAction, ConcreteAction):
    pass


class ReadResponse(BaseModel):
    game: Game

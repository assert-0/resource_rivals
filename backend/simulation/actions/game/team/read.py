from pydantic import BaseModel

from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.team_action import TeamAction
from simulation.team import Team


class ReadRequest(TeamAction, ConcreteAction):
    pass


class ReadResponse(BaseModel):
    team: Team

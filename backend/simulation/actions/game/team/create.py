from pydantic import BaseModel

from consts import TEAMS_NEUTRAL_ID
from simulation.actions.action import ConcreteAction
from simulation.actions.game.team.team_action import TeamAction
from simulation.team import Team


class CreateRequest(TeamAction, ConcreteAction):
    teamId: str = TEAMS_NEUTRAL_ID
    name: str


class CreateResponse(BaseModel):
    team: Team

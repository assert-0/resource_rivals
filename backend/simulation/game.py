from typing import Dict, Set
from uuid import uuid4

from pydantic import BaseModel, Field

from consts import TEAMS_NEUTRAL_ID
from entities.dynamic.buildings.capital import Capital
from simulation.consts import GameStates
from simulation.history import History
from simulation.map import Map
from simulation.team import Team


class Game(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    map: Map
    teams: Dict[str, Team] = Field(default_factory=dict)
    history: History = History()
    state: GameStates = GameStates.BEFORE_START
    activeTeamId: str = TEAMS_NEUTRAL_ID
    winningTeamId: str = TEAMS_NEUTRAL_ID

    @staticmethod
    def new_game(map_path: str) -> "Game":
        map = Map.from_file(map_path)
        return Game(map=map)

    def get_active_team(self) -> Team:
        return self.teams[self.activeTeamId]

    def register_team(self, name: str) -> Team:
        team = Team(name=name)
        self.teams[team.id] = team
        return team

    def start(self) -> None:
        self.state = GameStates.IN_PROGRESS
        self.activeTeamId = list(self.teams.keys())[0]

        self._mark_capitals()

    def stop(self, winning_team_id: str = TEAMS_NEUTRAL_ID) -> None:
        self.state = GameStates.FINISHED
        self.activeTeamId = TEAMS_NEUTRAL_ID
        self.winningTeamId = winning_team_id

    def _mark_capitals(self):
        capitals: Set[Capital] = {
            entity for entity in self.map.get_entities()
            if isinstance(entity, Capital)
        }

        if len(capitals) != len(self.teams):
            raise ValueError(
                "Number of capitals in map must be equal to number of teams"
            )

        for team, capital in zip(self.teams.values(), capitals):
            capital.teamId = team.id

        self.map.update_entities(capitals)

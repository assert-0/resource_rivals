from typing import Optional, List

from entities.dynamic.buildings.building import Building
from entities.dynamic.units.unit import Unit
from entities.dynamic.units.worker import Worker
from entities.entity import Entity
from simulation.consts import GameStates
from simulation.game import Game
from simulation.team import Team
from utils.math import Point


class Server:
    def __init__(self):
        self.games = {}

    # Game management

    def game_create(
            self,
            map_path: Optional[str] = None,
            map_name: Optional[str] = None,
    ) -> Game:
        game = Game.new_game(
            map_path=map_path, map_name=map_name,
        )
        self.games[game.id] = game
        return game

    def game_delete(self, game_id: str) -> None:
        if game_id not in self.games:
            raise ValueError(f"Game with id {game_id} not found")
        del self.games[game_id]

    def game_get_info(self, game_id: str) -> Game:
        return self._game_get(game_id)

    def game_start(self, game_id: str) -> None:
        game = self._game_get(game_id)
        game.start()

    def _game_expect_running(self, game_id: str) -> Game:
        game = self._game_get(game_id)
        if game.state != GameStates.IN_PROGRESS:
            raise ValueError(f"Game with id {game_id} is not running")

        return game

    def _game_get(self, game_id: str) -> Game:
        if game_id not in self.games:
            raise ValueError(f"Game with id {game_id} not found")
        return self.games[game_id]

    # Team management

    def team_create(self, game_id: str, name: str) -> Team:
        game = self._game_get(game_id)
        return game.register_team(name)

    def team_get_info(self, game_id: str, team_id: str) -> Team:
        return self._team_get(game_id, team_id)

    def team_get_visible_map(
            self, game_id: str, team_id: str
    ) -> List[List[Optional[List[Entity]]]]:
        game = self._game_expect_running(game_id)
        team = self._team_get(game_id, team_id)
        return team.get_visible_map(game.map)

    def team_end_turn(self, game_id: str, team_id: str) -> None:
        self._team_check_active(game_id, team_id)

        game = self._game_expect_running(game_id)
        game.end_turn()

    def _team_get(self, game_id: str, team_id: str) -> Team:
        game = self._game_get(game_id)
        if team_id not in game.teams:
            raise ValueError(f"Team with id {team_id} not found")
        return game.teams[team_id]

    def _team_check_active(self, game_id: str, team_id: str) -> None:
        game = self._game_expect_running(game_id)
        if team_id != game.get_active_team().id:
            raise ValueError(
                f"Team {team_id} is not active team ({game.activeTeamId})"
            )

    # Unit management

    def unit_get_reachable_sectors(
            self, game_id: str, team_id: str, unit_id: str
    ) -> List[Point]:
        self._team_check_active(game_id, team_id)
        self._unit_check_correct_team(game_id, team_id, unit_id)
        self._unit_check_not_moved(game_id, team_id, unit_id)

        game = self._game_expect_running(game_id)
        unit = self._unit_get(game_id, unit_id)

        return unit.calculate_reachable_sectors(game.map.sectors)

    def unit_move(
            self, game_id: str, team_id: str, unit_id: str,
            target_position: Point
    ) -> None:
        self._team_check_active(game_id, team_id)
        self._unit_check_correct_team(game_id, team_id, unit_id)
        self._unit_check_not_moved(game_id, team_id, unit_id)

        game = self._game_expect_running(game_id)
        team = self._team_get(game_id, team_id)
        unit = self._unit_get(game_id, unit_id)

        unit.act(target_position, game.map)
        game.movedUnits.add(unit.id)
        team.recalculate_visible_area(game.map)

    def unit_get_available_buildings(
            self, game_id: str, team_id: str, unit_id: str
    ) -> List[List[str]]:
        self._team_check_active(game_id, team_id)
        self._unit_check_correct_team(game_id, team_id, unit_id)
        self._unit_check_is_worker(game_id, unit_id)

        game = self._game_expect_running(game_id)
        unit = self._unit_get(game_id, unit_id)

        return unit.calculate_available_buildings(game)

    def unit_build(
            self, game_id: str, team_id: str, unit_id: str,
            building_type: str, building_namespace: str
    ) -> Building:
        self._team_check_active(game_id, team_id)
        self._unit_check_correct_team(game_id, team_id, unit_id)
        self._unit_check_is_worker(game_id, unit_id)

        game = self._game_expect_running(game_id)
        team = self._team_get(game_id, team_id)
        unit: Worker = self._unit_get(game_id, unit_id)  # type: ignore
        building = unit.build(building_type, building_namespace, game)

        team.recalculate_visible_area(game.map)

        return building

    def _unit_get(self, game_id: str, unit_id: str) -> Unit:
        game = self._game_expect_running(game_id)
        entity = game.map.expect_entity_by_id(unit_id)
        if not isinstance(entity, Unit):
            raise ValueError(
                f"Selected entity is not a unit: {entity.type}"
            )

        return entity

    def _unit_check_correct_team(
            self, game_id: str, team_id: str, unit_id: str
    ) -> None:
        unit = self._unit_get(game_id, unit_id)
        if unit.teamId != team_id:
            raise ValueError(f"Unit {unit_id} is not owned by team {team_id}")

    def _unit_check_not_moved(
            self, game_id: str, team_id: str, unit_id: str
    ) -> None:
        game = self._game_expect_running(game_id)
        if unit_id in game.movedUnits:
            raise ValueError(f"Unit {unit_id} has already moved this turn")

    def _unit_check_is_worker(self, game_id: str, unit_id: str) -> None:
        unit = self._unit_get(game_id, unit_id)
        if not isinstance(unit, Worker):
            raise ValueError(
                f"Only workers can build. Selected unit type: {unit.type}"
            )


server = Server()

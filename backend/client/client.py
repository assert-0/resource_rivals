from typing import List, Callable

import requests
from tabulate import tabulate

from consts import TEAMS_NEUTRAL_ID
from entities.entity import Entity
from simulation.game import Game
from simulation.team import Team
from utils.logger import get_logger
from utils.math import Point

logger = get_logger("client")


class Client:
    def __init__(self, api_prefix: str = "http://localhost:8000/api/v1"):
        self.api_prefix = api_prefix

    def game_create(self, map_name: str) -> Game:
        logger.debug("Creating game")

        create_game_url = f"{self.api_prefix}/game"
        response = requests.post(create_game_url, json={"mapName": map_name})

        if response.status_code != 200:
            raise ValueError(f"Error creating game: {response.json()}")

        try:
            game = Game(**response.json()["game"])
        except Exception as e:
            raise ValueError(f"Error creating game: {e}")

        logger.debug(f"Game created with id: {game.id}")

        return game

    def game_delete(self, game_id: str) -> None:
        logger.debug(f"Deleting game {game_id}")

        delete_game_url = f"{self.api_prefix}/game/{game_id}"
        response = requests.delete(delete_game_url)

        if response.status_code != 200:
            raise ValueError(f"Error deleting game: {response.json()}")

    def game_get_info(self, game_id: str) -> Game:
        logger.debug(f"Getting game info for game {game_id}")

        get_game_info_url = f"{self.api_prefix}/game/{game_id}"
        response = requests.get(get_game_info_url)

        if response.status_code != 200:
            raise ValueError(f"Error getting game info: {response.json()}")

        try:
            game_info = Game(**response.json()["game"])
        except Exception as e:
            raise ValueError(f"Error getting game info: {e}")

        logger.debug(f"Game info: {game_info}")

        return game_info

    def game_start(self, game_id: str) -> None:
        logger.debug(f"Starting game {game_id}")

        start_game_url = f"{self.api_prefix}/game/{game_id}/start"
        response = requests.post(start_game_url)

        if response.status_code != 200:
            raise ValueError(f"Error starting game: {response.json()}")

    def team_create(self, game_id: str, name: str) -> Team:
        logger.debug(f"Creating team with name {name}")

        create_team_url = f"{self.api_prefix}/game/{game_id}/team"
        response = requests.post(create_team_url, json={"name": name})

        if response.status_code != 200:
            raise ValueError(f"Error creating team: {response.json()}")

        try:
            team = Team(**response.json()["team"])
        except Exception as e:
            raise ValueError(f"Error creating team: {e}")

        team_id = team.id
        name = team.name

        logger.debug(f"Team created with id: {team_id} and name {name}")

        return team

    def team_get_info(self, game_id: str, team_id: str) -> Team:
        logger.debug(f"Getting team info for team {team_id}")

        get_team_info_url = f"{self.api_prefix}/game/{game_id}/team/{team_id}"
        response = requests.get(get_team_info_url)

        if response.status_code != 200:
            raise ValueError(f"Error getting team info: {response.json()}")

        try:
            team_info = Team(**response.json()["team"])
        except Exception as e:
            raise ValueError(f"Error getting team info: {e}")

        logger.debug(f"Team info: {team_info}")

        return team_info

    def team_get_visible_map(
            self, game_id: str, team_id: str
    ) -> List[List[Entity]]:
        logger.debug(f"Getting visible map for team {team_id}")

        get_visible_map_url = (
            f"{self.api_prefix}/game/{game_id}/team/{team_id}/visible-map"
        )
        response = requests.get(get_visible_map_url)

        if response.status_code != 200:
            raise ValueError(f"Error getting visible map: {response.json()}")

        try:
            visible_map = []
            for column in response.json()["sectors"]:
                visible_map.append([])
                for sector in column:
                    if sector is None:
                        visible_map[-1].append(None)
                        continue
                    elif not sector:
                        visible_map[-1].append([])
                        continue
                    entities = []
                    for entity in sector:
                        entities.append(Entity(**entity) if entity else None)
                    visible_map[-1].append(entities)
        except Exception as e:
            raise ValueError(f"Error getting visible map: {e}")

        logger.debug(f"Visible map: {visible_map}")

        return visible_map

    def team_end_turn(self, game_id: str, team_id: str) -> None:
        logger.debug(f"Ending turn for team {team_id}")

        end_turn_url = (
            f"{self.api_prefix}/game/{game_id}/team/{team_id}/"
            f"end-turn"
        )
        response = requests.post(end_turn_url)

        if response.status_code != 200:
            raise ValueError(f"Error ending turn: {response.json()}")

    def unit_get_reachable_sectors(
            self, game_id: str, team_id: str, unit_id: str
    ) -> List[Point]:
        logger.debug(f"Getting reachable sectors for unit {unit_id}")

        get_reachable_sectors_url = (
            f"{self.api_prefix}/game/{game_id}/team/{team_id}/unit/{unit_id}/"
            f"move/reachable-sectors"
        )
        response = requests.get(get_reachable_sectors_url)

        if response.status_code != 200:
            raise ValueError(
                f"Error getting reachable sectors: {response.json()}"
            )

        try:
            reachable_sectors = []
            for sector_coord in response.json()["sectors"]:
                reachable_sectors.append(Point(**sector_coord))
        except Exception as e:
            raise ValueError(f"Error getting reachable sectors: {e}")

        logger.debug(f"Reachable sectors: {reachable_sectors}")

        return reachable_sectors

    def unit_move(
            self, game_id: str, team_id: str, unit_id: str,
            target_position: Point
    ) -> None:
        logger.debug(f"Moving unit {unit_id} to {target_position}")

        move_unit_url = (
            f"{self.api_prefix}/game/{game_id}/team/{team_id}/unit/{unit_id}/"
            f"move"
        )
        response = requests.post(
            move_unit_url, json={
                "targetPosition": target_position.model_dump()
            }
        )

        if response.status_code != 200:
            raise ValueError(f"Error moving unit: {response.json()}")

    def unit_get_available_buildings(
            self, game_id: str, team_id: str, unit_id: str
    ) -> List[List[str]]:  # (namespace, type) tuples
        logger.debug(f"Getting available buildings for unit {unit_id}")

        get_available_buildings_url = (
            f"{self.api_prefix}/game/{game_id}/team/{team_id}/unit/{unit_id}/"
            f"build/avaliable-buildings"
        )
        response = requests.get(get_available_buildings_url)

        if response.status_code != 200:
            raise ValueError(
                f"Error getting available buildings: {response.json()}"
            )

        try:
            available_buildings = response.json()["buildings"]
        except Exception as e:
            raise ValueError(f"Error getting available buildings: {e}")

        logger.debug(f"Available buildings: {available_buildings}")

        return available_buildings

    def unit_build(
            self, game_id: str, team_id: str, unit_id: str,
            building_type: str, building_namespace: str
    ) -> None:
        logger.debug(f"Building {building_type} with unit {unit_id}")

        build_unit_url = (
            f"{self.api_prefix}/game/{game_id}/team/{team_id}/unit/{unit_id}/"
            f"build"
        )
        response = requests.post(
            build_unit_url, json={
                "buildingType": building_type,
                "buildingNamespace": building_namespace
            }
        )

        if response.status_code != 200:
            raise ValueError(f"Error building: {response.json()}")

    def visualize_map(
            self, sectors: List[List[Entity]], team_ids: List[str],
            visualization_function: Callable
    ):
        if TEAMS_NEUTRAL_ID not in team_ids:
            team_ids.insert(0, TEAMS_NEUTRAL_ID)
        out_data = []
        for x, column in enumerate(sectors):
            out_data.append([])
            for y, sector in enumerate(column):
                out_data[x].append(
                    visualization_function(sector, x, y, team_ids)
                )

        transposed = list(zip(*out_data))
        print(tabulate(transposed, headers=()))

    def visualize_map_verbose(
            self, sectors: List[List[Entity]], team_ids: List[str]
    ):
        def visualize_sector(
                sector: List[Entity], x: int, y: int, team_ids: List[str]
        ):
            if sector is not None:
                entities = [
                    (
                        entity.type, team_ids.index(entity.teamId)
                    ) for entity in sector
                ]
            else:
                entities = "Fog"

            return (
                f"(x: {x}, y: {y}), "
                f"entities: {entities}"
            )

        self.visualize_map(sectors, team_ids, visualize_sector)

    def visualize_map_compact(
            self, sectors: List[List[Entity]], team_ids: List[str]
    ):
        def visualize_sector(
                sector: List[Entity], x: int, y: int, team_ids: List[str]
        ):
            if sector:
                entities = ",".join([
                    f"{entity.type[0]}{team_ids.index(entity.teamId)}"
                    for entity in sector
                ])
            elif sector is not None:
                entities = "_"
            else:
                entities = "F"

            return f"{entities}"

        self.visualize_map(sectors, team_ids, visualize_sector)

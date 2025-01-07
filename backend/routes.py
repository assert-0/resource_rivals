from fastapi import APIRouter, Request, Response

from server import server
from simulation.actions.response import Response as GenericResponse
from simulation.actions.game.create import (
    CreateResponse as GameCreateResponse, CreateRequest as GameCreateRequest
)
from simulation.actions.game.read import ReadResponse as GameReadResponse

from simulation.actions.game.team.create import (
    CreateResponse as TeamCreateResponse, CreateRequest as TeamCreateRequest
)
from simulation.actions.game.team.get_visible_map import (
    GetVisibleMapResponse as TeamGetVisibleMapResponse
)
from simulation.actions.game.team.read import ReadResponse as TeamReadResponse

from simulation.actions.game.team.unit.build.create import (
    CreateResponse as BuildCreateResponse, CreateRequest as BuildCreateRequest
)
from simulation.actions.game.team.unit.build.get_available_buildings import (
    GetAvailableBuildingsResponse as UnitGetAvailableBuildingsResponse
)
from simulation.actions.game.team.unit.move.create import (
    CreateRequest as MoveCreateRequest
)
from simulation.actions.game.team.unit.move.get_reachable_sectors import (
    GetReachableSectorsResponse as UnitGetReachableSectorsResponse
)


api_router = APIRouter(prefix="/api/v1")


@api_router.post("/game", response_model=GameCreateResponse)
async def create_game(
        request: Request, response: Response
) -> GameCreateResponse:
    request = await request.json()
    parsed_request = GameCreateRequest(**request)

    try:
        created_game = server.create_game(map_path=parsed_request.mapName)
    except ValueError as e:
        response.status_code = 400
        return GameCreateResponse(error=str(e), game=None)

    return GameCreateResponse(game=created_game)


@api_router.get("/game/{game_id}", response_model=GameReadResponse)
async def read_game(game_id: str, response: Response) -> GameReadResponse:
    try:
        game = server.get_game(game_id)
    except ValueError as e:
        response.status_code = 400
        return GameReadResponse(error=str(e), game=None)

    return GameReadResponse(game=game)


@api_router.delete("/game/{game_id}", response_model=None)
async def delete_game(game_id: str, response: Response) -> GenericResponse:
    try:
        server.delete_game(game_id)
    except ValueError as e:
        response.status_code = 400
        return GenericResponse(error=str(e))

    return GenericResponse()


@api_router.post("/game/{game_id}/team/", response_model=TeamCreateResponse)
async def create_team(
        game_id: str, request: Request, response: Response
) -> TeamCreateResponse:
    request = await request.json()
    parsed_request = TeamCreateRequest(**request)

    try:
        created_team = server.get_game(game_id).register_team(
            name=parsed_request.teamName
        )
    except ValueError as e:
        response.status_code = 400
        return TeamCreateResponse(error=str(e), team=None)

    return TeamCreateResponse(team=created_team)


@api_router.get(
    "/game/{game_id}/team/{team_id}", response_model=TeamReadResponse
)
async def read_team(
        game_id: str, team_id: str, response: Response
) -> TeamReadResponse:
    try:
        team = server.get_game(game_id).teams[team_id]
    except ValueError as e:
        response.status_code = 400
        return TeamReadResponse(error=str(e), team=None)

    return TeamReadResponse(team=team)


@api_router.get(
    "/game/{game_id}/team/{team_id}/visible-map",
    response_model=TeamGetVisibleMapResponse
)
async def get_visible_map(
        game_id: str, team_id: str, response: Response
) -> TeamGetVisibleMapResponse:
    try:
        game = server.get_game(game_id)
        team = game.teams[team_id]
        visible_map = team.get_visible_map(game.map)
    except ValueError as e:
        response.status_code = 400
        return TeamGetVisibleMapResponse(error=str(e), sectors=None)

    return TeamGetVisibleMapResponse(sectors=visible_map)


@api_router.post(
    "/game/{game_id}/team/{team_id}/end-turn", response_model=None
)
async def end_turn(game_id: str, team_id: str, response: Response) -> None:
    pass


@api_router.post(
    "/game/{game_id}/team/{team_id}/unit/{unit_id}/build",
    response_model=BuildCreateResponse
)
async def create_building(
        game_id: str, team_id: str, unit_id: str, request: Request
) -> BuildCreateResponse:
    request = await request.json()
    parsed_request = BuildCreateRequest(**request)


@api_router.get(
    "/game/{game_id}/team/{team_id}/unit/{unit_id}/build/available-buildings",
    response_model=UnitGetAvailableBuildingsResponse
)
async def get_available_buildings(
        game_id: str, team_id: str, unit_id: str
) -> UnitGetAvailableBuildingsResponse:
    pass


@api_router.post(
    "/game/{game_id}/team/{team_id}/unit/{unit_id}/move",
    response_model=None
)
async def move_unit(
        game_id: str, team_id: str, unit_id: str, request: Request
) -> None:
    request = await request.json()
    parsed_request = MoveCreateRequest(**request)


@api_router.get(
    "/game/{game_id}/team/{team_id}/unit/{unit_id}/move/reachable-sectors",
    response_model=UnitGetReachableSectorsResponse
)
async def get_reachable_sectors(
        game_id: str, team_id: str, unit_id: str
) -> UnitGetReachableSectorsResponse:
    pass

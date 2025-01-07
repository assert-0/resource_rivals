from fastapi import APIRouter, Request, Response

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


api_router = APIRouter(prefix="/api/v1")


@api_router.post("/game", response_model=GameCreateResponse)
async def create_game(request: Request) -> GameCreateResponse:
    request = await request.json()
    parsed_request = GameCreateRequest(**request)


@api_router.get("/game/{game_id}", response_model=GameReadResponse)
async def read_game(game_id: str) -> GameReadResponse:
    pass


@api_router.delete("/game/{game_id}", response_model=None)
async def delete_game(game_id: str, response: Response) -> None:
    pass


@api_router.post("/game/{game_id}/team/", response_model=TeamCreateResponse)
async def create_team(game_id: str, request: Request) -> TeamCreateResponse:
    request = await request.json()
    parsed_request = TeamCreateRequest(**request)


@api_router.get(
    "/game/{game_id}/team/{team_id}", response_model=TeamReadResponse
)
async def read_team(game_id: str, team_id: str) -> TeamReadResponse:
    pass


@api_router.get(
    "/game/{game_id}/team/{team_id}/visible-map",
    response_model=TeamGetVisibleMapResponse
)
async def get_visible_map(
        game_id: str, team_id: str
) -> TeamGetVisibleMapResponse:
    pass

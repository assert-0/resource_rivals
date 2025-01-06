from fastapi import APIRouter
from fastapi.responses import JSONResponse

from simulation.actions.game.create import CreateResponse as GameCreateResponse
from simulation.actions.game.read import ReadResponse as GameReadResponse
from simulation.actions.game.team.create import (
    CreateResponse as TeamCreateResponse
)
from simulation.actions.game.team.read import ReadResponse as TeamReadResponse

api_router = APIRouter(prefix="/api/v1")


@api_router.post("/game")
async def create_game() -> GameCreateResponse:
    pass


@api_router.get("/game/{game_id}")
async def read_game(game_id: str) -> GameReadResponse:
    pass


@api_router.post("/game/{game_id}/team/")
async def create_team(game_id: str) -> TeamCreateResponse:
    pass


@api_router.get("/game/{game_id}/team/{team_id}")
async def read_team(game_id: str, team_id: str) -> TeamReadResponse:
    pass

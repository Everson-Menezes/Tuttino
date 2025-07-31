from fastapi import APIRouter, HTTPException
from typing import List

from application.game_service import GameService
from domain.entities.game import Game

router = APIRouter()
game_service = GameService()

@router.get("/games", response_model=List[Game])
async def get_games():
    return await game_service.list_games()

@router.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: int):
    game = await game_service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

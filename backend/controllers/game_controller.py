# controllers/games_controller.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from interface.game_service_interface import IGameService
from application.game_service import GameService
from domain.entities.game import Game

router = APIRouter()

def get_game_service() -> IGameService:
    return GameService()

@router.get("/games", response_model=List[Game])
async def get_games(service: IGameService = Depends(get_game_service)):
    return await service.list_games()

@router.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: int, service: IGameService = Depends(get_game_service)):
    game = await service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

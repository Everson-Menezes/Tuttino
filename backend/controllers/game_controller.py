from fastapi import APIRouter
from typing import List
from domain.entities.game import Game

router = APIRouter()

# Mock de jogos para exemplo
GAMES = [
    Game(id=1, title="Aventura no Espaço", description="Uma jornada intergaláctica", thumbnail_url="http://example.com/space.jpg", difficulty="hard", language="en", tags=["aventura", "espaço"], is_active=True, created_at="2023-01-01T00:00:00Z", updated_at="2023-01-02T00:00:00Z"),
    Game(id=2, title="Tutino Quest", description="Uma jornada épica", thumbnail_url="http://example.com/quest.jpg", difficulty="medium", language="pt-br", tags=["aventura", "quest"], is_active=True, created_at="2023-01-01T00:00:00Z", updated_at="2023-01-02T00:00:00Z"),
    Game(id=3, title="Desafio de Programação", description="Teste suas habilidades de codificação", thumbnail_url="http://example.com/coding.jpg", difficulty="easy", language="en", tags=["programação", "desafio"], is_active=True, created_at="2023-01-01T00:00:00Z", updated_at="2023-01-02T00:00:00Z"),
]
@router.get("/games", response_model=List[Game])
async def get_games():
    return GAMES

@router.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: int):
    for game in GAMES:
        if game.id == game_id:
            return game
    return {"error": "Game not found"}

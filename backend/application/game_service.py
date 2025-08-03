from typing import List, Optional

from domain.entities.game import Game
from infrastructure.repositories.games_repository import GameRepository


from interface.services.game_service_interface import IGameService

class GameService(IGameService):
    def __init__(self):
        self.repository = GameRepository()

    async def list_games(self) -> List[Game]:
        return self.repository.list_all()

    async def get_game_by_id(self, game_id: int) -> Optional[Game]:
        return self.repository.get_by_id(game_id)

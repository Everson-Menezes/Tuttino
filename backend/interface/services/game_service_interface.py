from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.game import Game

class IGameService(ABC):

    @abstractmethod
    async def list_games(self) -> List[Game]:
        """Return all available games"""
        pass

    @abstractmethod
    async def get_game_by_id(self, game_id: int) -> Optional[Game]:
        """Return a game by its ID, or None if not found"""
        pass

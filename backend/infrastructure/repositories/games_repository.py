from typing import Dict, Optional, List
from datetime import datetime

from domain.entities.game import Game

class GameRepository:
    def __init__(self):
        self._games: Dict[int, Game] = {
            1: Game(
                id=1,
                title="Aventura no Espaço",
                description="Uma jornada intergaláctica",
                thumbnail_url="http://example.com/space.jpg",
                difficulty="hard",
                language="en",
                tags=["aventura", "espaço"],
                is_active=True,
                created_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                updated_at=datetime.fromisoformat("2025-01-02T00:00:00"),
            ),
            2: Game(
                id=2,
                title="Tutino Quest",
                description="Uma jornada épica",
                thumbnail_url="http://example.com/quest.jpg",
                difficulty="medium",
                language="pt-br",
                tags=["aventura", "quest"],
                is_active=True,
                created_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                updated_at=datetime.fromisoformat("2025-01-02T00:00:00"),
            ),
            3: Game(
                id=3,
                title="Desafio de Programação",
                description="Teste suas habilidades de codificação",
                thumbnail_url="http://example.com/coding.jpg",
                difficulty="easy",
                language="en",
                tags=["programação", "desafio"],
                is_active=True,
                created_at=datetime.fromisoformat("2025-01-01T00:00:00"),
                updated_at=datetime.fromisoformat("2025-01-02T00:00:00"),
            )
        }

    def get_by_id(self, game_id: int) -> Optional[Game]:
        return self._games.get(game_id)

    def list_all(self) -> List[Game]:
        return list(self._games.values())

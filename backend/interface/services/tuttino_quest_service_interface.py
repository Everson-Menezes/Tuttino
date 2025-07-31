# application/tuttino_quest_service.py
from typing import Optional, List

from domain.entities.tuttino_quest import TuttinoQuest
from interface.repositories.tuttino_quest_repository_interface import ITuttinoQuestRepository

class TuttinoQuestService:
    def __init__(self, repository: ITuttinoQuestRepository):
        self._repository = repository

    async def get_all_quests(self) -> List[TuttinoQuest]:
        return self._repository.list_all()

    async def get_quest_by_id(self, quest_id: int) -> Optional[TuttinoQuest]:
        return self._repository.get_by_id(quest_id)

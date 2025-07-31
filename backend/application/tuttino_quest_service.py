from typing import List, Optional
from domain.entities.tuttino_quest import TuttinoQuest
from interface.tuttino_quest_service_interface import ITuttinoQuestService
from infrastructure.repositories.tuttino_quest_repository import TuttinoQuestRepository

class TuttinoQuestService(ITuttinoQuestService):

    def __init__(self):
        self.repository = TuttinoQuestRepository()

    async def get_all_quests(self) -> List[TuttinoQuest]:
        return await self.repository.list_all()

    async def get_quest_by_id(self, quest_id: int) -> Optional[TuttinoQuest]:
        return await self.repository.get_by_id(quest_id)

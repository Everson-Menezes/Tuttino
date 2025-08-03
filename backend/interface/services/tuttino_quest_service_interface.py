from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.tuttino_quest import TuttinoQuest

class ITuttinoQuestService(ABC):
    @abstractmethod
    async def get_all_quests(self) -> List[TuttinoQuest]:
        pass

    @abstractmethod
    async def get_quest_by_id(self, quest_id: int) -> Optional[TuttinoQuest]:
        pass

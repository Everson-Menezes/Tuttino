# interface/tuttino_quest_repository_interface.py
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.tuttino_quest import TuttinoQuest

class ITuttinoQuestRepository(ABC):

    @abstractmethod
    def list_all(self) -> List[TuttinoQuest]:
        """
        Returns a list of all TuttinoQuest entities.
        """
        pass

    @abstractmethod
    def get_by_id(self, quest_id: int) -> Optional[TuttinoQuest]:
        """
        Returns a TuttinoQuest entity by its ID or None if not found.
        """
        pass

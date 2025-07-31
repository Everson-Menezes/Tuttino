# domain/entities/tuttino_quest.py
from pydantic import BaseModel
from typing import List
from domain.entities.tuttino_quest_stage import Stage

class TuttinoQuest(BaseModel):
    id: int
    title: str
    description: str
    language: str
    thumbnail_url: str
    is_active: bool
    stages: List[Stage]

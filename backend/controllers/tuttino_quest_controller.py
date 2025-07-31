# controllers/tuttino_quest_controller.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from application.tuttino_quest_service import TuttinoQuestService
from domain.entities.tuttino_quest import TuttinoQuest
from interface.repositories.tuttino_quest_repository_interface import ITuttinoQuestRepository
from infrastructure.repositories.tuttino_quest_repository import TuttinoQuestRepository

router = APIRouter(prefix="/tuttino-quests", tags=["TuttinoQuests"])

def get_repository() -> ITuttinoQuestRepository:
    return TuttinoQuestRepository()

def get_service(repo: ITuttinoQuestRepository = Depends(get_repository)) -> TuttinoQuestService:
    return TuttinoQuestService(repo)

@router.get("/", response_model=List[TuttinoQuest])
async def list_quests(service: TuttinoQuestService = Depends(get_service)):
    return await service.get_all_quests()

@router.get("/{quest_id}", response_model=TuttinoQuest)
async def get_quest(quest_id: int, service: TuttinoQuestService = Depends(get_service)):
    quest = await service.get_quest_by_id(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return quest

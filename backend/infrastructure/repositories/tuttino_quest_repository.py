# infrastructure/repositories/tuttino_quest_repository.py
from typing import Optional, List
from domain.entities.tuttino_quest import TuttinoQuest
from domain.entities.tuttino_quest_stage import Stage
from interface.repositories.tuttino_quest_repository_interface import ITuttinoQuestRepository

class TuttinoQuestRepository(ITuttinoQuestRepository):
    def __init__(self):
        self._quests = {
            1: TuttinoQuest(
                id=1,
                title="Tutino Quest",
                description="Uma jornada épica",
                language="pt-br",
                thumbnail_url="http://example.com/quest.jpg",
                is_active=True,
                stages=[
                    Stage(
                        id=1,
                        title="Animais da Fazenda",
                        challenge="Qual desses é uma vaca?",
                        type="multiple_choice",
                        options=["Cachorro", "Vaca", "Gato", "Cavalo"],
                        correct_answer="Vaca",
                        hint="Ela faz muuu",
                        language="pt-br"
                    ),
                    Stage(
                        id=2,
                        title="Formas e Cores",
                        challenge="Qual dessas é uma bola vermelha?",
                        type="multiple_choice",
                        options=["Bola Azul", "Quadrado Vermelho", "Bola Vermelha", "Triângulo Verde"],
                        correct_answer="Bola Vermelha",
                        hint="É redonda e da cor do morango",
                        language="pt-br"
                    ),
                    Stage(
                        id=3,
                        title="Números Básicos",
                        challenge="Quanto é 2 + 2?",
                        type="multiple_choice",
                        options=["3", "4", "5", "22"],
                        correct_answer="4",
                        hint="É um número par depois do 3",
                        language="pt-br"
                    )
                ]
            )
        }

    def list_all(self) -> List[TuttinoQuest]:
        return list(self._quests.values())

    def get_by_id(self, quest_id: int) -> Optional[TuttinoQuest]:
        return self._quests.get(quest_id)

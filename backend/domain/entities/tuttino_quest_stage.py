# domain/entities/stage.py
from pydantic import BaseModel
from typing import List, Optional


class Stage(BaseModel):
    id: int
    title: str
    challenge: str  # Texto do desafio
    type: str  # Ex: "multiple_choice", "audio", "image_label"
    options: Optional[List[str]] = None  # Apenas para tipos com alternativas
    correct_answer: str  # Pode ser texto, áudio ou imagem dependendo do tipo
    hint: Optional[str] = None  # Dica para a criança
    language: str  # Idioma da fase

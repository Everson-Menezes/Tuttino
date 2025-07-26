from pydantic import BaseModel
from typing import List

class Game(BaseModel):
    id: int
    title: str
    description: str
    thumbnail_url: str
    difficulty: str
    language: str
    tags: List[str]
    is_active: bool
    created_at: str
    updated_at: str
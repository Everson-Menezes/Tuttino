from datetime import datetime
from pydantic import BaseModel

class Game(BaseModel):
    id: int
    title: str
    description: str
    thumbnail_url: str
    difficulty: str
    language: str
    tags: list[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
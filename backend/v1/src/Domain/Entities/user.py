from dataclasses import dataclass

from backend.v1.src.Domain.Entities import Email
from backend.v1.src.Domain.Entities import Password
from backend.v1.src.Domain.Entities import Profile


@dataclass
class User:
    id: str
    email: Email
    password: Password
    name: str
    profile: Profile
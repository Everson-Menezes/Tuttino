from dataclasses import dataclass

from v1.src.Domain.Entities import Email
from v1.src.Domain.Entities import Password
from v1.src.Domain.Entities import Profile


@dataclass
class User:
    id: str
    email: Email
    password: Password
    name: str
    profile: Profile
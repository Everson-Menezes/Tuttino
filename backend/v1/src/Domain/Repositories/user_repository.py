from typing import Optional

from backend.v1.src.Domain.Entities.user import User



class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users = {}

    def add(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if str(user.email) == str(email):
                return user
        return None

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

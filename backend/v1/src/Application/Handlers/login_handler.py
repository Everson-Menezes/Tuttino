

from backend.v1.src.Application.Services.user_service import UserService


class LoginHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, email: str, password: str) -> str:
        return self.user_service.login(email, password)

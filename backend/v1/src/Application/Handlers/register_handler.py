from v1.src.Application.DTOs.userDTO import UserDTO
from v1.src.Application.Services.user_service import UserService


class RegisterHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, email: str, password: str, name: str, profile: str) -> UserDTO:
        return self.user_service.register(email, password, name, profile)

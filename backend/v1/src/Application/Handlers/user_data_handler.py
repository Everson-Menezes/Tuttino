from backend.v1.src.Application.DTOs.userDTO import UserDTO
from backend.v1.src.Application.Services.user_service import UserService

class UserDataHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def handle(self, user_id: str) -> UserDTO:
        return self.user_service.get_user_data(user_id)

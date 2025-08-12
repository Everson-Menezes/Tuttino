from v1.src.Application.DTOs.userDTO import UserDTO
from v1.src.Domain.Entities.user import User

def user_to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        email=str(user.email),
        name=user.name,
        profile=str(user.profile)
    )

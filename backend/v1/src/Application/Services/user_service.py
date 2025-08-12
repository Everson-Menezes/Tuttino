import uuid


from backend.v1.src.Application.DTOs.userDTO import UserDTO, user_to_dto
from backend.v1.src.Domain.Entities.user import User
from backend.v1.src.Domain.Entities.email import Email
from backend.v1.src.Domain.Entities.password import Password
from backend.v1.src.Domain.Entities.profile import Profile


class UserService:
    def __init__(self, user_repo: IUserRepository, auth_service: AuthenticationService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def register(self, email: str, password: str, name: str, profile: str) -> UserDTO:
        if self.user_repo.find_by_email(email):
            raise ValueError("Email already registered")

        password_obj = self.auth_service.hash_password(password)
        user = User(
            id=str(uuid.uuid4()),
            email=Email(email),
            password=Password(plain_password=password),
            name=name,
            profile=Profile(profile)
        )
        self.user_repo.add(user)
        return user_to_dto(user)
    
    def login(self, email: str, password: str) -> str:
        user = self.user_repo.find_by_email(Email(email))
        if not user or not user.password.verify(password):
            raise ValueError("Invalid credentials")

        return self.auth_service.generate_jwt(user.id)

    def get_user_data(self, user_id: str) -> UserDTO:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user_to_dto(user)
import bcrypt
from datetime import datetime, timedelta
import jwt

from backend.v1.src.Domain.Repositories.user_repository import IUserRepository
from backend.v1.src.Domain.Entities.user import User

class AuthenticationService:

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def hash_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    def generate_jwt(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

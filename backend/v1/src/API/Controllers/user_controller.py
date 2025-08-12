from typing import Optional
import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Header

from v1.src.Domain.Repositories.user_repository import InMemoryUserRepository
from v1.src.Domain.Services.authentication_service import AuthenticationService
from v1.src.Application.Services.user_service import UserService
from v1.src.Application.Handlers.register_handler import RegisterHandler
from v1.src.Application.Handlers.login_handler import LoginHandler
from v1.src.Application.Handlers.user_data_handler import UserDataHandler
from v1.src.Infrastructure.Configurations.jwt_config import JWTConfig

router = APIRouter()

user_repo = InMemoryUserRepository()
auth_service = AuthenticationService(JWTConfig.SECRET_KEY)
user_service = UserService(user_repo, auth_service)

register_handler = RegisterHandler(user_service)
login_handler = LoginHandler(user_service)
user_data_handler = UserDataHandler(user_service)

def verify_token(authorization: Optional[str] = Header(None)) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing or invalid")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWTConfig.SECRET_KEY, algorithms=[JWTConfig.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: dict):
    try:
        user_dto = register_handler.handle(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            profile=data["profile"]
        )
        return user_dto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/login")
def login(data: dict):
    try:
        token = login_handler.handle(email=data["email"], password=data["password"])
        return {"token": token}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.get("/me")
def get_user(current_user_id: str = Depends(verify_token)):
    try:
        user_dto = user_data_handler.handle(current_user_id)
        return user_dto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

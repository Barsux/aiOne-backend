from fastapi import APIRouter
from fastapi import Depends
from app.models.auth import InputUser, FillInputUser, User
from app.services.auth import AuthService
from typing import List

router = APIRouter(
    prefix="/auth"
)


@router.post("/")
def sign(
    input_user: InputUser,
    service: AuthService = Depends()
) -> str:
    return service.signinup(input_user)


@router.get("/{token}")
def get_user(
    token: str,
    service: AuthService = Depends()
) -> User:
    return service.get_user(token)


@router.post("/{token}")
def update_user(
    token: str,
    updates: FillInputUser,
    service: AuthService = Depends()
) -> User:
    return service.update_user(token, updates)


@router.get("/users/{token}")
def get_all_users(
        token: str,
        service: AuthService = Depends()
) -> List[User]:
    return service.get_users(token)
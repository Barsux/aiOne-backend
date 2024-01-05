import secrets

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from typing import List

from app import tables
from app.database import get_session
from app.models.auth import User, InputUser, FillInputUser


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def signinup(self, input_user: InputUser) -> str:
        query = self.session.query(tables.User)
        user = query.filter_by(email=input_user.email).first()
        if user:
            if user.password == input_user.password:
                return user.api
            raise HTTPException(status_code=400, detail="Неверный пользователь.")
        na = "Н/Д"
        user = tables.User(
            email=input_user.email,
            password=input_user.password,
            first_name=na,
            last_name=na,
            phone=na,
            first_address=na,
            second_address=na,
            is_client=True,
            api=secrets.token_urlsafe(32)
        )
        self.session.add(user)
        self.session.commit()
        return user.api

    def get_user(self, token: str) -> User:
        query = self.session.query(tables.User)
        query = query.filter_by(api=token)
        query = query.first()
        print(query)
        if not query:
            raise HTTPException(status_code=401, detail="Ошибка авторизации.")
        return query

    def get_users(self, token: str) -> List[User]:
        user = self.get_user(token)
        query = self.session.query(tables.User)
        return query.all()

    def update_user(self, token: str, updates: FillInputUser) -> User:
        user = self.get_user(token)
        for key, value in updates.dict().items():
            setattr(user, key, value)
        self.session.commit()
        return user
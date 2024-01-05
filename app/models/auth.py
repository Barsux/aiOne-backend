from datetime import date
from pydantic import BaseModel, field_validator, ValidationError


class InputUser(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        if '@' not in email or '.' not in email:
            raise ValidationError("Неверный формат электронной почты.")
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValidationError("Пароль должен быть не менее 8 символов.")
        return password


class FillInputUser(BaseModel):
    first_name: str
    last_name: str
    phone: str
    first_address: str
    second_address: str
    is_client: bool

    @field_validator("phone")
    @classmethod
    def validate_phone_rus(cls, phone: str):
        if phone[0] not in ['+', '8']: return False
        if len(phone) not in [11, 12]: return False
        if not phone.isnumeric(): return False
        if len(phone) == 11:
            if phone[1:3] != '79': return False
        else:
            if phone[0:2] != '89': return False
        return True


class User(InputUser, FillInputUser):
    id: int
    api: str | None

    class Config:
        from_attributes = True

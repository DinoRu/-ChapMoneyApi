import uuid
from datetime import datetime

from pydantic import EmailStr, BaseModel, field_validator, model_validator, constr, validator

from app.schemas.base import CustomConfig
from app.schemas.transaction import TransferOut



class Email(CustomConfig):
    email: EmailStr

class LoginCredentials(Email, BaseModel):
    password: str

class Phone(BaseModel):
    phone: str

class Name(BaseModel):
    name: str


class CreateUser(Email, Name, Phone, BaseModel):
    password: str


class ShowUserOwnTransaction(CustomConfig):
    amount: float
    timestamp: datetime


class User(CustomConfig):
    guid: uuid.UUID
    email: EmailStr | None
    phone: str | None
    name: str | None

    transactions: list[TransferOut]

class UserInfo(BaseModel):
    email: EmailStr
    phone: str
    name: str

    class Config:
        from_attributes = True





class UpdatePassword(BaseModel):
    old_password: str
    password: str
    confirm_password: str

class SetPinRequest(BaseModel):
    pin: str

    @field_validator("pin")
    def validate_pin(cls, value):
        if not value.isdigit():
            raise ValueError("PIN doit contenir uniquement des chiffres.")
        if len(value) != 4:
            raise ValueError("PIN doit avoir exactement 4 chiffres.")
        return value


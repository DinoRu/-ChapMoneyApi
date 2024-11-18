import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class AccountBase(BaseModel):
	account_name: str
	account_number: str
	account_type: str


class CreateAccount(AccountBase):
	pass


class UpdateAccountRequest(BaseModel):
	account_name: Optional[str] = None
	account_number: Optional[str] = None
	account_type: Optional[str] = None

class UpdateAccountNameRequest(BaseModel):
	account_name: Optional[str] = None


class UpdateAccountNumberRequest(BaseModel):
	account_number: Optional[str] = None


class AccountOut(CustomConfig, AccountBase):
	guid: uuid.UUID
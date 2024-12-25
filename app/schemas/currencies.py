import uuid

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class CurrencyBase(BaseModel):
	name: str
	full_name: str
	symbol: str

class CreateCurrency(CustomConfig):
	name: str

class UpdateCurrency(CustomConfig):
	name: str


class CurrencyResponse(CustomConfig, CurrencyBase):
	guid: uuid.UUID

import uuid

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class CurrencyBase(BaseModel):
	name: str
	full_name: str
	symbol: str

class CreateCurrency(CustomConfig, CurrencyBase):
	pass

class UpdateCurrency(CustomConfig, CurrencyBase):
	pass


class CurrencyResponse(CustomConfig, CurrencyBase):
	guid: uuid.UUID

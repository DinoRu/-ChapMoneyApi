import uuid

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class ExchangeRateBase(BaseModel):
	from_currency_id: uuid.UUID
	to_currency_id: uuid.UUID
	rates: float


class CreateExchangeRate(ExchangeRateBase):
	pass


class ExchangeRateOut(CustomConfig, ExchangeRateBase):
	guid: uuid.UUID


class ExchangeRateCreateRequest(BaseModel):
	rate: float
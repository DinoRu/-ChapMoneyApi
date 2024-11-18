import uuid

from pydantic import BaseModel

from app.schemas.currencies import CurrencyResponse
from app.schemas.receiving_method import ReceivingMethodOut
from app.schemas.sending_method import SendingMethodOut


class CountryBase(BaseModel):
	name: str
	code: str
	calling_phone: str
	flag_url: str | None


class CreateCountry(CountryBase):
	currency_id: uuid.UUID

class UpdateCountryName(BaseModel):
	name: str
	

class CountryResponse(CountryBase):
	guid: uuid.UUID
	currency: CurrencyResponse
	receiving_methods: list[ReceivingMethodOut]
	sending_methods: list[SendingMethodOut]

	class Config:
		from_attributes = True

import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class ReceivingMethodBase(BaseModel):
	name: str
	required_card_number: bool

class CreateReceivingMethod(ReceivingMethodBase):
	pass


class UpdateReceivingMethod(BaseModel):
	name: Optional[str]
	required_card: Optional[bool]

class ReceivingMethodOut(CustomConfig, ReceivingMethodBase):
	guid: uuid.UUID
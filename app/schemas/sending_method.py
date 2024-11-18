import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class SendingMethodBase(BaseModel):
	name: str
	number: str
	owner_name: str

class CreateSendingMethod(SendingMethodBase):
	country_id: uuid.UUID


class UpdateSendingMethod(BaseModel):
	name: str


class SendingMethodOut(CustomConfig, SendingMethodBase):
	guid: uuid.UUID


class SendingMethodCreateRequest(BaseModel):
	name: str
	number: str
	owner_name: str

class SendingMethodUpdateRequest(BaseModel):
	name: Optional[str] = None
	number: Optional[str] = None
	owner_name: Optional[str] = None

class SendingMethodUpdateNameRequest(BaseModel):
	name: Optional[str] = None

class SendingMethodUpdateNumberRequest(BaseModel):
	number: Optional[str] = None

class SendingMethodUpdateOwnerNameRequest(BaseModel):
	owner_name: Optional[str] = None


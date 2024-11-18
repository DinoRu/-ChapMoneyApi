import uuid

from pydantic import BaseModel

from app.schemas.base import CustomConfig


class TransferFeesBase(BaseModel):
	sender_country_id: uuid.UUID
	receiver_country_id: uuid.UUID
	fee_percentage: float


class TransferFeesCreate(TransferFeesBase):
	pass


class UpdateTransferFees(BaseModel):
	fees: float

class TransferFeesOut(CustomConfig, TransferFeesBase):
	guid: uuid.UUID


class FeesSchema(BaseModel):
	fees: float
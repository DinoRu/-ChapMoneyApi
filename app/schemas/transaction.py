import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    email: EmailStr
    name: str
    phone: str

    class Config:
        from_attributes = True


class TransactionStatus(str, Enum):
    INITIATED = "initiated"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Transfer(BaseModel):
    amount: float
    from_country: str
    to_country: str
    payment_method: str
    recipient_name: str
    recipient_phone: str
    receiving_method: str


class TransferOut(BaseModel):
    guid: uuid.UUID
    from_country: str
    to_country: str
    amount: float
    converted_amount: float
    final_amount: float
    payment_method: str
    recipient_name: str
    recipient_phone: str
    receiving_method: str
    status: TransactionStatus
    sender: UserInfo

    class Config:
        from_attributes = True

class AdminTransferOut(TransferOut):
    sender: UserInfo
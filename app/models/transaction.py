import uuid
from datetime import datetime
from enum import Enum as pyEnum
from sqlalchemy import ForeignKey, Enum, Float, DateTime, DECIMAL, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.database import Base

class TimedBaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=sql.func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now())


class TransactionStatus(str, pyEnum):
    INITIATED = "initiated"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"



class Account(TimedBaseModel):
    __tablename__ = "accounts"

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                                            default=uuid.uuid4)
    account_name: Mapped[str] = mapped_column(nullable=False, index=True)
    account_number: Mapped[str] = mapped_column(nullable=False)
    account_type: Mapped[str] = mapped_column(nullable=True)
    # methods: Mapped[list["SendingMethod"]] = relationship("SendingMethod", back_populates="account")



class Country(TimedBaseModel):
    __tablename__ = "countries"

    guid: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True,
                                            default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    code: Mapped[str] = mapped_column(nullable=True, unique=True)
    calling_phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    flag_url: Mapped[str | None] = mapped_column(nullable=True)
    currency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("currencies.guid"))
    currency: Mapped["Currency"] = relationship("Currency", back_populates='countries')
    receiving_methods: Mapped[list["ReceivingMethod"]] = relationship("ReceivingMethod",
                                                                      back_populates="country")
    sending_methods: Mapped[list["SendingMethod"]] = relationship("SendingMethod",
                                                                  back_populates="country")



class Currency(TimedBaseModel):
    __tablename__ = 'currencies'

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True,
                                            default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str] = mapped_column(nullable=True)
    countries: Mapped[list["Country"]] = relationship("Country", back_populates='currency')


class CurrencyPrice(TimedBaseModel):
    __tablename__ = "currency_prices"

    guid: Mapped[uuid.UUID] = (mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                               default=uuid.uuid4))
    current_id: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), ForeignKey(
        "currencies.guid"))
    price = Mapped[float]
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    currency = relationship('Currency', backref='prices')


class ExchangeRates(TimedBaseModel):
    __tablename__ = "conversion_rates"

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                                            default=uuid.uuid4)
    from_currency_id: Mapped["Currency"] = mapped_column(ForeignKey("currencies.guid"))
    to_currency_id: Mapped["Currency"] = mapped_column(ForeignKey("currencies.guid"))
    from_currency: Mapped['Currency'] = relationship("Currency", foreign_keys=[from_currency_id])
    to_currency: Mapped['Currency'] = relationship("Currency", foreign_keys=[to_currency_id])

    rates: Mapped[float] = mapped_column(nullable=False)




class TransferFee(TimedBaseModel):
    __tablename__ = "transfer_fees"

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                                            default=uuid.uuid4)

    sender_country_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("countries.guid"))
    receiver_country_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("countries.guid"))
    fee_percentage: Mapped[float] = mapped_column(Float, nullable=False)

    sender_country: Mapped["Country"] = relationship("Country", foreign_keys=[sender_country_id])
    receiver_country: Mapped["Country"] = relationship("Country", foreign_keys=[
        receiver_country_id])



class SendingMethod(TimedBaseModel):
    __tablename__ = "sending_methods"

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                                            default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=False, index=True)
    number: Mapped[str] = mapped_column(nullable=False)
    owner_name: Mapped[str] = mapped_column(nullable=False)
    country_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey("countries.guid"))
    country: Mapped["Country"] = relationship("Country", back_populates="sending_methods")



class ReceivingMethod(TimedBaseModel):
    __tablename__ = "receiving_methods"

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                                            default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    country_id: Mapped['Country'] = mapped_column(ForeignKey("countries.guid"))
    required_card_number: Mapped[bool | None] = mapped_column(nullable=True, default=False)
    country: Mapped['Country'] = relationship("Country", back_populates='receiving_methods')


class Transaction(TimedBaseModel):
    __tablename__ = 'transactions'

    guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
                                            default=uuid.uuid4)
    amount: Mapped[float] = mapped_column(nullable=False)
    converted_amount: Mapped[float]
    final_amount: Mapped[float]
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.guid"))
    from_country: Mapped[str] = mapped_column(nullable=False)
    to_country: Mapped[str] = mapped_column(nullable=False)
    recipient_name: Mapped[str] = mapped_column(nullable=False)
    recipient_phone: Mapped[str] = mapped_column(nullable=False)
    payment_method: Mapped[str] = mapped_column(nullable=False)
    receiving_method: Mapped[str] = mapped_column(nullable=False)
    sender: Mapped["User"] = relationship("User", back_populates='transactions')
    status: Mapped[TransactionStatus] \
        = mapped_column(Enum(TransactionStatus), default=TransactionStatus.INITIATED)
    completed_at: Mapped[str | None] = mapped_column(default=None)

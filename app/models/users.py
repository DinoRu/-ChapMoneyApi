import uuid

import bcrypt
from passlib.context import CryptContext
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_utils import UUIDType, EmailType

from app.database import Base
from app.models.transaction import Transaction

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class User(Base):
	__tablename__ = "users"

	guid: Mapped[uuid.UUID] = mapped_column(UUIDType(binary=False), primary_key=True, index=True,
											default=uuid.uuid4)
	email: Mapped[str] = mapped_column(EmailType, unique=True)
	phone: Mapped[str] = mapped_column(nullable=True, unique=True)
	password: Mapped[str]
	name: Mapped[str] = mapped_column(String, nullable=True, unique=True, index=True)
	pin: Mapped[str] = mapped_column(nullable=True)
	transactions: Mapped[list[Transaction]] = relationship("Transaction",
														   back_populates="sender",
														   lazy="selectin")


	def __repr__(self):
		return f"User {self.email}"

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import symbol
from sqlalchemy_utils import Currency

from app.models.transaction import Currency as CurrencyModel
from app.repositories.base import BaseRepository
from app.schemas.currencies import CreateCurrency


class CurrencyRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=CurrencyModel)

	async def create(self, instance: CurrencyModel, session: AsyncSession) -> CurrencyModel:
		return await super().create(instance=instance, session=session)


currency_repository = CurrencyRepository()
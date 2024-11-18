from collections.abc import Iterable
from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hash_password import HashPassword
from app.models.users import User
from app.schemas.users import CreateUser
from app.utils.messages import messages

hash_password = HashPassword()

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_schema: CreateUser) -> User:
        user = User(**user_schema.dict())
        hashed_password = hash_password.create_hash(user.password)
        user.password = hashed_password
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_or_create(self, email: str, user_schema: Optional[CreateUser] = None) -> User:
        user = await self.get(email=email)
        if not user and user_schema:
            try:
                return await self.create(user_schema)
            except IntegrityError:
                await self.db.rollback()
                raise Exception(messages.USER_ALREADY_EXISTS)
        return user

    async def get(self, **kwargs) -> Optional[User]:
        query = select(User)
        if kwargs:
            query = self.set_filters(query=query, kwargs=kwargs)
        results = await self.db.execute(query)
        return results.scalars().first()

    async def all(self) -> Iterable[User]:
        results = await self.db.execute(select(User))
        return results.scalars().all()

    async def filter(self, order_by: Optional[str], **kwargs) -> Iterable[User]:
        query = select(User)
        if kwargs:
            query = self.set_filters(query=query, kwargs=kwargs)
        if order_by:
            query = self.set_order_by(query=query, order_by=order_by)
        results = await self.db.execute(query)
        return results.scalars().all()

    async def update(self, user: User) -> User:
        await self.db.merge(user)
        await self.db.commit()
        return user

    async def bulk_update(self, users: Iterable[User]) ->Iterable[User]:
        for user in users:
            await self.db.merge(user)
        await self.db.commit()
        return users

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

    async def bulk_delete(self, users: Iterable[User]) -> None:
        for user in users:
            await self.db.delete(user)
        await self.db.commit()

    def set_filters(self, query, kwargs: dict) -> select:
        filters = []
        for field, value in kwargs.items():
            if value:
                try:
                    if field.endswith("__gt"):
                        model_field = getattr(User, field[:-4])
                        filters.append(model_field > value)
                    elif field.endswith("__gte"):
                        model_field = getattr(User, field[:-5])
                        filters.append(model_field >= value)
                    elif field.endswith("__lt"):
                        model_field = getattr(User, field[:-4])
                        filters.append(model_field < value)
                    elif field.endswith("__lte"):
                        model_field = getattr(User, field[:-5])
                        filters.append(model_field <= value)
                    else:
                        model_field = getattr(User, field)
                        filters.append(model_field == value)
                except AttributeError:
                    return query
        return query.filter(and_(*filters))


    def set_order_by(self, query, order_by: str):
        if order_by.startswith("-"):
            order_by_field = getattr(User, order_by[1:]).desc()
        else:
            order_by_field = getattr(User, order_by)
        return query.order_by(order_by_field)



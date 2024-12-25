import uuid
from datetime import datetime

import jwt
from asyncpg.pgproto.pgproto import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.users import User as UserModel
from app.repositories.users import UserRepository
from app.schemas.users import CreateUser, UpdatePassword
from app.utils.messages import messages


class UserController:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def create_user(self, user_schema: CreateUser) -> UserModel:
       email = user_schema.email
       if await self.user_repo.get(email=email):
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=messages.USER_ALREADY_EXISTS
           )
       return await self.user_repo.create(user_schema=user_schema)

    async def get_user_or_404(self, email: str):
        user = await self.user_repo.get(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=messages.USER_NOT_FOUND
            )
        return user

    async def update_password(self, email: str, change_password_schema: UpdatePassword):
        user = await self.get_user_or_404(email=email)
        if not user.verify_password(password=change_password_schema.old_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.WRONG_OLD_PASSWORD
            )
        if user.verify_password(password=change_password_schema.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.NEW_PASSWORD_SIMILAR_OLD
            )
        user.password = user.get_hashed_password()
        await self.user_repo.update(user=user)

    async def reset_password(self, token: str, new_password: str):
        if not self.verify_token(token=token):
            raise HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                detail=messages.INVALID_TOKEN
            )
        email = self.get_email_from_token(token)
        user = await self.get_user_or_404(email=email)
        user.password = user.get_hashed_password()
        await self.user_repo.update(user=user)

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            token_data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            is_active = token_data.get("is_active")
            return bool(is_active)
        except jwt.ExpiredSignatureError:
            raise False
        except jwt.InvalidTokenError:
            return False

    @staticmethod
    def create_token(email: str) -> str:
        # expires_at = (datetime.now() + timedelta(hours=settings.token_expires_hours)).timestamp()
        payload = {"email": email, "is_active": True}
        return jwt.encode(payload=payload, key=settings.secret_key,
                          algorithm=settings.algorithm)

    @staticmethod
    def create_refresh_token(email: str) -> str:
        expires_at = (datetime.now() + timedelta(hours=settings.refresh_token_expires)).timestamp()
        payload = {"exp": expires_at, "email": email, "is_active": True}
        return jwt.encode(payload=payload, key=settings.secret_key,
                          algorithm=settings.algorithm)

    @staticmethod
    def get_email_from_token(token: str) -> str:
        token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
        return token_data.get('email')

    async def create_pin(self, pin: str, user: UserModel):
        return await self.user_repo.set_pin_code(pin=pin, user=user)

    async def verify_code_pin(self, pin: str, user: UserModel):
        return await self.user_repo.verify_pin_code(pin=pin, user=user)

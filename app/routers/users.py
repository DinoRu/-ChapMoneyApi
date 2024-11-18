from fastapi import APIRouter, status, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer, JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hash_password import HashPassword
from app.config import settings
from app.controllers.users import UserController
from app.database import get_session
from app.dependencies import get_current_user
from app.schemas.users import CreateUser, LoginCredentials, UpdatePassword, Email, User
from app.utils.mail import html_reset_password_mail, send_mail
from app.utils.messages import messages

router = APIRouter(prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not "
																						  "found"}})
security = HTTPBearer()
hashed_password = HashPassword()

access_security = JwtAccessBearer(secret_key=settings.authjwt_secret_key)
refresh_security = JwtRefreshBearer(secret_key=settings.authjwt_secret_key)


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Registration")
async def register(user_schema: CreateUser, session: AsyncSession = Depends(get_session)):
	user_controller = UserController(db=session)
	await user_controller.create_user(user_schema=user_schema)
	return {"email": user_schema.email, 'detail': messages.USER_CREATED}


@router.post('/login', status_code=status.HTTP_200_OK, summary="Authorization, get tokens")
async def login(login_credentials: LoginCredentials,
				session: AsyncSession = Depends(get_session),
				):
	user_controller = UserController(db=session)
	user = await user_controller.get_user_or_404(email=login_credentials.email)
	if not hashed_password.verify_hash(login_credentials.password, user.password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.WRONG_PASSWORD)
	access_token = user_controller.create_token(email=user.email)
	refresh_token = user_controller.create_refresh_token(email=user.email)
	return {
		"access_token": access_token,
		"refresh_token": refresh_token
	}

@router.delete("/logout/", status_code=status.HTTP_200_OK, summary="Logout")
async def logout(credentials: HTTPAuthorizationCredentials = Security(security)):
	return {"detail": messages.USER_LOGOUT}

@router.post("/change-password/", status_code=status.HTTP_202_ACCEPTED, summary="Change password")
async def change_password(data: UpdatePassword, session: AsyncSession = Depends(get_session), credentials:
		HTTPAuthorizationCredentials = Security(security)):
	user_controller = UserController(db=session)
	token = credentials.credentials
	if data.password != data.confirm_password:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=messages.PASSWORDS_NOT_MATCH
		)
	email = user_controller.get_email_from_token(token=token)
	await user_controller.update_password(
		email=email,
		change_password_schema=data
	)
	return {"detail": messages.PASSWORD_UPDATED}

@router.post("/forgot-password/",
			 status_code=status.HTTP_202_ACCEPTED,
			 summary="Send request for reset password token mail")
async def forgot_password(data: Email, session: AsyncSession = Depends(get_session)):
	user_controller = UserController(db=session)
	user = await user_controller.get_user_or_404(email=data.email)
	reset_password_token = user_controller.create_token(email=user.email)
	subject = "Reset password"
	recipients = [user.email]
	body = html_reset_password_mail(reset_password_token=reset_password_token)
	await send_mail(subject=subject, recipients=recipients, body=body)
	return {"detail": messages.RESET_PASSWORD_MAIL_SENT}

@router.post("/reset-password/{token}", status_code=status.HTTP_202_ACCEPTED,
			 summary="Reset password")
async def reset_password(token: str, data: UpdatePassword, session: AsyncSession = Depends(
	get_session)):
	user_controller = UserController(db=session)
	if data.password != data.confirm_password:
		raise HTTPException(
			status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
			detail=messages.PASSWORDS_NOT_MATCH
		)
	await user_controller.reset_password(token=token, new_password=data.password, session=session)
	return {"detail": messages.PASSWORD_RESET}

@router.get("/info/", status_code=status.HTTP_200_OK,
			summary="User info")
async def get_user_info(current_user: User = Depends(get_current_user)):
	return User.from_orm(current_user)
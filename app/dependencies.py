from fastapi import Security, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.users import UserController
from app.database import get_session

security  = HTTPBearer()

async def get_current_user(
		credentials: HTTPAuthorizationCredentials = Security(security),
		session: AsyncSession = Depends(get_session)
):
	token = credentials.credentials
	user_controller = UserController(session)
	try:
		email = user_controller.get_email_from_token(token)
		user = await user_controller.get_user_or_404(email)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token or user not found."
		)
	return user
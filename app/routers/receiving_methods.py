import uuid

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.receiving_method import receive_payment_controller
from app.database import get_session
from app.schemas.receiving_method import UpdateReceivingMethod, CreateReceivingMethod

router = APIRouter(
	prefix="/receiving-methods",
	tags=['Receiving methods'],
	responses={404: {'description': 'not found'}}
)

@router.get("/all", status_code=status.HTTP_200_OK, summary="Get all receiving methods")
async def all_methods(
		session: AsyncSession = Depends(get_session)
):
	return await receive_payment_controller.all(session=session)

@router.get("/methods/{method_id}", status_code=status.HTTP_200_OK, summary="Get method")
async def get_or_404(
		method_id: str,
		session: AsyncSession = Depends(get_session)
):
	return await receive_payment_controller.get_or_404(session=session, guid=method_id)


@router.post('/create/{country_name}/method',
			 status_code=status.HTTP_201_CREATED, summary="Create method")
async def create_method(
		country_name: str,
		request: CreateReceivingMethod,
		session: AsyncSession = Depends(get_session)):
	return await receive_payment_controller.create(
		session=session,
		country_name=country_name,
		method_name=request.name,
		required_card=request.required_card_numbe
	)


@router.put('/update/{method_id}', status_code=status.HTTP_200_OK, summary='Update method name')
async def update_method_name(
		method_id: uuid.UUID,
		data: UpdateReceivingMethod,
		session: AsyncSession = Depends(get_session)
):
	return await receive_payment_controller.update_method(
		session=session,
		guid=method_id,
		data=data
	)

@router.delete("/delete/{method_id}", status_code=status.HTTP_200_OK, summary="Delete method")
async def delete_method(
		method_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	return await receive_payment_controller.delete(
		session=session,
		method_id=method_id
	)
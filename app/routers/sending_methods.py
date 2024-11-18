from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.sending_method import send_payment_controller
from app.database import get_session
from app.schemas.sending_method import CreateSendingMethod, UpdateSendingMethod, \
	SendingMethodCreateRequest, SendingMethodUpdateRequest

router = APIRouter(
	prefix="/send-methods",
	tags=['Send methods'],
	responses={404: {'description': 'not found'}}
)

@router.get("/methods/{country_name}",
			status_code=status.HTTP_200_OK,
			summary="List of sending methods by country name")
async def list_sending_methods(
		country_name: str,
		session: AsyncSession = Depends(get_session)
):
	return await send_payment_controller.get_sending_methods(
		session, country_name
	)

@router.post("/method/{country_name}/create",
			 status_code=status.HTTP_201_CREATED,
			 summary="Create new sending method")
async def create_sending_method(
		country_name: str,
		request: SendingMethodCreateRequest,
		session: AsyncSession = Depends(get_session)
):
	return await send_payment_controller.add_sending_method(
		session=session,
		country_name=country_name,
		name=request.name,
		number=request.number,
		owner_name=request.owner_name
	)


@router.put("/methods/{method_guid}/update",
			  status_code=status.HTTP_200_OK,
			  summary="Update sending method by GUID")
async def update_sending_method(
		method_guid: str,
		request: SendingMethodUpdateRequest,
		session: AsyncSession = Depends(get_session)
):
	return await send_payment_controller.modify_sending_method(
		session=session,
		method_guid=method_guid,
		name=request.name,
		number=request.number,
		owner_name=request.owner_name
	)

@router.delete("/methods/{method_guid}",
			   status_code=status.HTTP_200_OK,
			   summary="Delete sending method by GUID")
async def delete_sending_method(
		method_guid: str,
		session: AsyncSession = Depends(get_session)
):
	return await send_payment_controller.remove_sending_method(
		method_guid=method_guid,
		session=session
	)
from pydantic import BaseModel


class CustomConfig(BaseModel):
	class Config:
		from_attributes = True

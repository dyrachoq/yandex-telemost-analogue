from uuid import UUID
from pydantic import BaseModel, Field




class RoomCreateSchema(BaseModel):
    name: str = Field(max_length=15, min_length=3)

class RoomGetSchema(RoomCreateSchema):
    id: UUID
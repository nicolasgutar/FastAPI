from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")

# Base schema
class CropDataSchema(BaseModel):
    state_name: str
    district_name: str
    crop_year: int
    season: str
    crop: str
    area: float
    production: float

    class Config:
        orm_mode = True

# Request schema for creating new records
class RequestCropData(BaseModel):
    parameter: CropDataSchema = Field(...)

# Response schema for returning records
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

    class Config:
        orm_mode = True
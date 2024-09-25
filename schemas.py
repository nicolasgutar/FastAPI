from typing import List, Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field

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
class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[Any] = None

    class Config:
        orm_mode = True
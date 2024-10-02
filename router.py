from fastapi import APIRouter, Depends, Path, Query
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestCropData, Response
import methods

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/')
async def create_crop_data(crop_data: RequestCropData, db: Session = Depends(get_db)):
    created_data = methods.create_crop_data(db, crop_data.parameter)
    return Response(code='200', status='Ok', message="Crop_data created successfully", result=created_data).dict(exclude_none=True)

@router.get("/")
async def get_data(skip: int = Query(0), limit: int = Query(100), db: Session = Depends(get_db)):
    _data = methods.get_data(db, skip, limit)
    return Response(code='200', status='Ok', message="Crop_data fetched successfully", result=_data).dict(exclude_none=True)
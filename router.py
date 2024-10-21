from fastapi import APIRouter, HTTPException, Depends, Path, Query
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import CropDataSchema, RequestCropData, Response
import methods

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/db')
async def create_crop_data_db(crop_data: RequestCropData, db: Session = Depends(get_db)):
    created_data = methods.create_crop_data(db, crop_data.parameter)
    return Response(code='200', status='Ok', message="Crop_data created successfully", result=created_data).dict(exclude_none=True)

@router.post('/s3')
async def create_crop_data_s3(crop_data: RequestCropData):
    data = crop_data.dict()
    result = methods.save_to_s3(data, bucket_name='user-08-smm-ueia-so', object_name='crop_data.json')
    if result['status'] == 'success':
        return Response(code='200', status='Ok', message=result['message'], result=data).dict(exclude_none=True)
    else:
        raise HTTPException(status_code=500, detail=result['message'])

@router.get("/")
async def get_data(skip: int = Query(0), limit: int = Query(100), db: Session = Depends(get_db)):
    _data = methods.get_data(db, skip, limit)
    return Response(code='200', status='Ok', message="Crop_data fetched successfully", result=_data).dict(exclude_none=True)
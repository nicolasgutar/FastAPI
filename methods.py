from sqlalchemy.orm import Session
from model import CropData
from schemas import CropDataSchema


#get all data
def get_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CropData).offset(skip).limit(limit).all()

#create an entry
def create_crop_data(db: Session, crop_data: CropDataSchema):
    db_crop_data = CropData(state_name=crop_data.state_name, district_name=crop_data.district_name,
                            crop_year=crop_data.crop_year, season=crop_data.season, crop=crop_data.crop,
                            area=crop_data.area, production=crop_data.production)
    db.add(db_crop_data)
    db.commit()
    db.refresh(db_crop_data)
    return db_crop_data

#delete an entry
def remove_crop_data(db: Session, id: int):
    crop_data = db.query(CropData).filter(CropData.id == id).first()
    db.delete(crop_data)
    db.commit()
    return crop_data

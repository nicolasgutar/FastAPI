from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

# Database setup
DATABASE_URL = "postgresql://user:password@localhost:5433/crop_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# CropData model
class CropData(Base):
    __tablename__ = "cropdata"
    id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String(255))
    district_name = Column(String(255))
    crop_year = Column(Integer)
    season = Column(String(255))
    crop = Column(String(255))
    area = Column(Float)
    production = Column(Float)

# Pydantic model for request body
class CropDataCreate(BaseModel):
    state_name: str
    district_name: str
    crop_year: int
    season: str
    crop: str
    area: float
    production: float

# Pydantic model for response
class CropDataResponse(BaseModel):
    id: int
    state_name: str
    district_name: str
    crop_year: int
    season: str
    crop: str
    area: float
    production: float

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET endpoint to fetch first 1000 records
@app.get("/cropdata", response_model=list[CropDataResponse])
def read_cropdata(db: Session = Depends(get_db)):
    try:
        cropdata = db.query(CropData).limit(1000).all()
        return cropdata
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST endpoint to add new records
@app.post("/cropdata", response_model=CropDataResponse)
def create_cropdata(cropdata: CropDataCreate, db: Session = Depends(get_db)):
    db_cropdata = CropData(**cropdata.dict())
    try:
        db.add(db_cropdata)
        db.commit()
        db.refresh(db_cropdata)
        return db_cropdata
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
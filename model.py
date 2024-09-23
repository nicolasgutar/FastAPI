from sqlalchemy import Column, Integer, String, Float
from config import Base


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
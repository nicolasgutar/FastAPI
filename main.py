from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# Database setup
DATABASE_URL = "postgresql://user:password@localhost:5433/crop_db"

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

# Dependency to get DB connection
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

# GET endpoint to fetch first 1000 records
@app.get("/cropdata", response_model=list[CropDataResponse])
def read_cropdata(db: psycopg2.extensions.connection = Depends(get_db)):
    try:
        with db.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM cropdata LIMIT 10")
            cropdata = cursor.fetchall()
            return cropdata
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST endpoint to add new records
@app.post("/cropdata", response_model=CropDataResponse)
def create_cropdata(cropdata: CropDataCreate, db: psycopg2.extensions.connection = Depends(get_db)):
    try:
        with db.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO cropdata (state_name, district_name, crop_year, season, crop, area, production)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, state_name, distrgitict_name, crop_year, season, crop, area, production
                """,
                (cropdata.state_name, cropdata.district_name, cropdata.crop_year, cropdata.season, cropdata.crop, cropdata.area, cropdata.production)
            )
            db.commit()
            new_cropdata = cursor.fetchone()
            return new_cropdata
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
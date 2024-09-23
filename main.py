from fastapi import FastAPI
import model
from config import engine
import router

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcoe home"}


app.include_router(router.router, prefix="/cropdata", tags=["cropdata"])
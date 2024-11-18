from dotenv import load_dotenv
from src.db_connection import init_db,get_collection
from fastapi import FastAPI
from route.profile_teacher_route import router

# Load environment variables from .env file
load_dotenv()
app = FastAPI()

# Initialize MongoDB client at app startup
@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(router)
@app.get("/")
def root():
    return {"message": "API is running"}

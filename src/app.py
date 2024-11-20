from dotenv import load_dotenv
from src.db_connection import init_db,get_collection
from fastapi import FastAPI, File, UploadFile
import shutil
from typing import Optional
import os

from src.route.profile_teacher_route import router as teacher_router
from src.route.profile_student_route import router as student_router
from src.route.profile_admin_route import router as admin_router
from src.route.dashboard_teacher_route import router as teacher_dashboard_router
from src.route.dashboard_student_route import router as student_dashboard_router
from src.route.aprove_admin_route import router as admin_aprovel_router


# Load environment variables from .env file
load_dotenv()
app = FastAPI()

# Initialize MongoDB client at app startup
@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(teacher_router)
app.include_router(student_router)
app.include_router(admin_router)
app.include_router(teacher_dashboard_router)
app.include_router(student_dashboard_router)
app.include_router(admin_aprovel_router)
@app.get("/")
def root():
    return {"message": "API is running"}



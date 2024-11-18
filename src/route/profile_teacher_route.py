from fastapi import APIRouter, HTTPException
# from src.model.profile_model import TeacherSchema
from ..model.profile_model import TeacherSchema

from ..db_connection import get_collection

collection = get_collection("teachers")

router = APIRouter()



@router.post("/login/teacher", status_code=201)
async def login_teacher(teacher:TeacherSchema):
    
    try:
        # Insert data into MongoDB
        result = collection.insert_one(teacher)
        return {"message": "Teacher login successfully", 'status_code':201}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) )

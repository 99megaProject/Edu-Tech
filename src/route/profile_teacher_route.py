from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from bson.json_util import dumps
from datetime import date, datetime
import os
import shutil

from ..db_connection import get_collection
from ..utils.img_upload import upload_img_to_cloudinary
from ..utils.random_generate import get_random_string 
from ..utils.send_email import send_email
from ..model.dashboard_teacher_model import TeacherDashboard


collection = get_collection("profile_teachers")

router = APIRouter()

# teacher register 
@router.post("/register/teacher", status_code=201)
async def register_teacher(
    name: str = Form(...),
    dob: date = Form(...),
    gender: str = Form(...),
    aadhar_no: int = Form(...),
    department: str = Form(...),
    ph_no: int = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Validation
        if ph_no < 1000000000 or ph_no > 9999999999:
            raise HTTPException(status_code=400, detail="Invalid phone number")
        if aadhar_no < 100000000000 or aadhar_no > 999999999999:
            raise HTTPException(status_code=400, detail="Invalid aadhar number")
        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Invalid email")

        file_location = f"temp_{file.filename}"

        # Save the file temporarily
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        avatar = upload_img_to_cloudinary(file_location, 'profile_teacher')

        teacher = {
            "name": name,
            "dob": dob.isoformat(),  # Convert date object to ISO 8601 string
            "gender": gender,
            "avatar": avatar,
            "aadhar_no": aadhar_no,
            "department": department,
            "ph_no": ph_no,
            "email": email,
            "address": address
        }

        teacher['username'] = get_random_string()
        teacher['password'] = get_random_string()
        teacher['last_update'] = datetime.utcnow().isoformat()  # Add a timestamp

        result = collection.insert_one(teacher)

        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to register teacher")
        
        # Creating and adding data into another collection
        dashboard_colle = get_collection("dashboard_teachers")

        dash_data = {
            "username": teacher['username'],
            "name": name,
        }

        instance = TeacherDashboard(**dash_data)
        dash_res = dashboard_colle.insert_one(instance.dict())

        if not dash_res.acknowledged:
            collection.delete_one({'username': teacher['username']})
            raise HTTPException(status_code=500, detail="Failed to register teacher")

        send_email(email,'Teacher registration successfully', f"Your username is {teacher['username']} and password is {teacher['password']}")

        os.remove(file_location)

        return {"message": "Teacher registered successfully", 'status_code': 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# teacher login - by teacher
@router.get("/teacher/login", status_code=200)
def teacher_login(username:str, password:str):
    try:
        result = collection.find_one({'username':username, 'password':password})
        if result==None:
            return { "message" : "User not found" , "status_code":404}
        else :
            return { "message" : "Teacher found successfully", "status_code":200, 'data' : dumps(result)}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# teacher delete id - by admin
@router.delete("/teacher/delete", status_code=200)
def teacher_delete(username:str):
    try:
        result = collection.delete_one({'username':username })
        if result.deleted_count==0:
            return { "message" : "Teacher not found" , "status_code":404}
        else :
            return { "message" : "Teacher delete successfully", "status_code":200, 'data' : dumps(result)}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# teacher find - by  anyone
@router.get("/teacher", status_code=200)
def teacher_find(name:str):
    try:
        result = collection.find({'username':username })
        if result==None:
            return { "message" : "Teacher not found" , "status_code":404}
        else :
            return { "message" : "Teacher found successfully", "status_code":200, 'data' : dumps(result)}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

#teacher update - by teacher
@router.put("/teacher/update", status_code=200)
def teacher_update( username:str, update_data:dict):
    try:

        if "username" in update_data:
            return { "message" : "username can not be changed", "status_code":400}

        result = collection.update_one({'username':username}, {"$set" : update_data})

        # Check if the document was updated
        if result.modified_count > 0:
            return { "message" : "Teacher updated successfully", "status_code":200}
        else:
            return { "message" : "No changed found", "status_code":400}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
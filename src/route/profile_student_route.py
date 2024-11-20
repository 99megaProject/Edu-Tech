from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from bson.json_util import dumps
from datetime import date, datetime
import os
import shutil

from ..db_connection import get_collection
from ..utils.img_upload import upload_img_to_cloudinary
from ..utils.random_generate import get_random_string 
from ..utils.send_email import send_email
from ..model.dashboard_student_model import StudentDashboard

collection = get_collection("profile_students")

router = APIRouter()

# Student register 
@router.post("/register/student", status_code=201)
async def register_teacher(
    name: str = Form(...),
    clg_roll: int = Form(...),
    uni_roll: int = Form(...), 
    dob: date = Form(...),
    gender: str = Form(...),
    aadhar_no: int = Form(...),
    ph_no: int = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    father_name: str = Form(...),
    mother_name: str = Form(...),
    course: str = Form(...),
    year: int   = Form(...),
    subjects : list[str] = Form(...),
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

        avatar = upload_img_to_cloudinary(file_location, 'profile_student')

        student = {
            'name': name,
            'clg_roll': clg_roll,
            'uni_roll':  uni_roll,
            'dob': dob.isoformat(),
            'gender':gender,
            'aadhar_no': aadhar_no,
            'ph_no': ph_no,
            'email': email,
            'address': address,
            'father_name': father_name,
            'mother_name': mother_name,
            'course': course,
            'year': year,
            'subjects' : subjects,
            'avatar': avatar
        }

        student['password'] = get_random_string()
        student['last_update'] = datetime.utcnow().isoformat()  # Add a timestamp

        result = collection.insert_one(student)

        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to register student")


        # Creating and adding data into another collection
        dashboard_colle = get_collection("dashboard_students")

        dash_data = {
            "clg_roll": clg_roll,
            "name": name,
            "subjects" : subjects,
            "course":course,
            "year":year
        }

        instance = StudentDashboard(**dash_data)
        dash_res = dashboard_colle.insert_one(instance.dict())

        if not dash_res.acknowledged:
            dashboard_colle.delete_one({'clg_roll': clg_roll})
            raise HTTPException(status_code=500, detail="Failed to register teacher")

        send_email(email,'Student registration successfully', f"Your college roll no is {student['clg_roll']} and password is {student['password']}")

        os.remove(file_location)

        return {"message": "Student registered successfully", 'status_code': 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Student login - by student
@router.get("/student/login", status_code=200)
def student_login(clg_roll:int, password:str):
    try:
        result = collection.find_one({'clg_roll':clg_roll, 'password':password})
        if result==None:
            return { "message" : "Student not found" , "status_code":404}
        else :
            return { "message" : "Student found successfully", "status_code":200, 'data' : dumps(result)}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Student delete id - by admin
@router.delete("/student/delete", status_code=200)
def student_delete(clg_roll:int):
    try:
        result = collection.delete_one({'clg_roll':clg_roll })
        if result.deleted_count==0:
            return { "message" : "Student not found" , "status_code":404}
        else :
            return { "message" : "Student delete successfully", "status_code":200}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    


#Student update - by student
@router.put("/student/update", status_code=200)
def student_update( clg_roll:int, update_data:dict):
    try:
        
        result = collection.update_one({'clg_roll':clg_roll}, {"$set" : update_data})
        print(result.acknowledged)
        # Check if the document was updated
        if result.modified_count > 0:
            return { "message" : "Student updated successfully", "status_code":200}
        else:
            return { "message" : "No changed found", "status_code":400}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


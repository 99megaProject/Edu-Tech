from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from bson.json_util import dumps
from datetime import date, datetime
import os
import shutil

from ..db_connection import get_collection
from ..utils.img_upload import upload_img_to_cloudinary
from ..utils.random_generate import get_random_string 
from ..utils.send_email import send_email


collection = get_collection("profile_admin")

router = APIRouter()

# admin register 
@router.post("/register/admin", status_code=201)
async def register_admin(
    name: str = Form(...), 
    dob: date = Form(...),
    gender: str = Form(...),
    aadhar_no: int = Form(...),
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

        avatar = upload_img_to_cloudinary(file_location, 'profile_admin')

        admin = {
            'name': name,
            'dob': dob.isoformat(),
            'gender':gender,
            'aadhar_no': aadhar_no,
            'ph_no': ph_no,
            'email': email,
            'address': address
        }

        admin['username'] = get_random_string()
        admin['password'] = get_random_string()
        admin['last_update'] = datetime.utcnow().isoformat()  # Add a timestamp

        result = collection.insert_one(admin)

        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to register student")

        send_email(email,'Admin registration successfully', f"Your username is {admin['username']} and password is {admin['password']}")

        os.remove(file_location)

        return {"message": "Admin registered successfully", 'status_code': 201}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# admin login - by admin
@router.get("/admin/login", status_code=200)
def admin_login(clg_roll:int, password:str):
    try:
        result = collection.find_one({'clg_roll':clg_roll, 'password':password})
        if result==None:
            return { "message" : "Student not found" , "status_code":404}
        else :
            return { "message" : "Student found successfully", "status_code":200, 'data' : dumps(result)}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# admin delete id - by admin
@router.delete("/admin/delete", status_code=200)
def admin_delete(username:str):
    try:
        result = collection.delete_one({'username':username })
        if result.deleted_count==0:
            return { "message" : "admin not found" , "status_code":404}
        else :
            return { "message" : "admin delete successfully", "status_code":200}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

#admin update - by another admin
@router.put("/admin/update", status_code=200)
def admin_update( username:str, update_data:dict):
    try:
    
        if "username" in update_data:
            return { "message" : "username can not be changed", "status_code":400}

        result = collection.update_one({'username':username}, {"$set" : update_data})
        # Check if the document was updated
        if result.modified_count > 0:
            return { "message" : "Admin updated successfully", "status_code":200}
        else:
            return { "message" : "No changed found", "status_code":400}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# admin find - by  anyone
@router.get("/admin", status_code=200)
def admin_find(name:str):
    try:
         
        result = collection.find({ "name" : name })
        # print(result)
        if result:
            return { "message" : "Admin found successfully", "status_code":200, 'data' : dumps(result)}
        else :
            return { "message" : "Admin not found" , "status_code":404}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    



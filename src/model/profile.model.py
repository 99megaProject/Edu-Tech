from pydantic import BaseModel, Field, HttpUrl  
from typing import List, Optional, Dict
from datetime import datetime

class TeacherSchema(BaseModel):
    name: str
    username:str = Field(..., unique=True)
    dob:datetime
    gender:str
    avatar: Optional[HttpUrl] = None  
    aadhar_no : int
    department:str
    ph_no:int 
    email: str = None
    address : str = None
    password: str
    last_update :datetime = Field(default_factory = datetime.utcnow)



class StudentSchema(BaseModel):
    name: str
    clg_roll: str = Field(..., unique=True)  
    uni_roll: str = Field(..., unique=True)  
    dob: datetime
    father_name: str
    mother_name: str
    course: str
    year: int  
    avatar: Optional[HttpUrl] = None  
    phone_no: int
    email_id: str   
    addhaar_id: int = Field(..., unique=True)
    address: Optional[str] = None
    subjects : Optional[List[str]] = None
    last_update :datetime = Field(default_factory = datetime.utcnow)



class Test(BaseModel):
    title:str
    no_of_ques:int
    ques: List[{"question":str,"options":List[str],"answer":str}]
    deadline: datetime
    created_at :datetime = Field(default_factory = datetime.utcnow)
    available : List[str]


class TeacherDashboard(BaseModel):
    _id : str
    available : str
    test: List[Dict] = []
    message : List[Dict]  = []
    matterial : Dict = {}
    profile : Dict = {}



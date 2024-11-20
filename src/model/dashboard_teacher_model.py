from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime

# Define a separate model for 'ques'
class Question(BaseModel):
    ques: str
    opt: List[str]
    ans: str
    mark: int = Field(..., gt=0, description="Marks must be positive")

class Test(BaseModel):
    test_id:str
    title: str
    no_of_ques: int = Field(..., gt=0, description="Number of questions must be positive")
    ques: List[Question]
    available: List[str]
    time: int = Field(..., gt=0, description="Time must be positive")
    attempted: int = Field(0, description="Number of attempts, default is 0")
    deadline: datetime
    created_at:datetime
    last_updated_at:datetime
   

class TeacherDashboard(BaseModel):
    username:str
    name:str
    available : str = 'Available'
    test: List[Test] = []
    message : List[Dict]  = []
    matterial : Dict = {}
    



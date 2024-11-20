from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime


class StudentDashboard(BaseModel):
    clg_roll: int
    name:str
    course : str
    year : int 
    test: List = []
    ask : List = []
    subjects : List = []
    message : List[Dict]  = []
    matterial : Dict = {}
    
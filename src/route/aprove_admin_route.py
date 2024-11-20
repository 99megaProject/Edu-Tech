from fastapi import APIRouter, HTTPException
from bson.json_util import dumps

from ..db_connection import get_collection
# from ..route.profile_teacher_route import 

router = APIRouter()

collection = get_collection('admin_aprovels')

@router.post('/admin/aprove')
def admin_aprovel(data:dict, req_type : str):
    try:
        new_data = {
            'data' : data,
            'req_type' : req_type
        }
        res = collection.insert_one(new_data)
        return { "message" : "Request saved successfully", 'status_code' : 201}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/admin/request')
def get_all_admin():
    try:
        res = collection.find()
        return { 'status_code' : 200, "data" : dumps(res)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
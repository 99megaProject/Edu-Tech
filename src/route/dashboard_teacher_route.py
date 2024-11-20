from fastapi import APIRouter,HTTPException
from typing import  List
from datetime import date,datetime,timedelta
from bson.json_util import dumps


from ..db_connection import get_collection
from ..model.dashboard_teacher_model import Test,Question
from ..utils.random_generate import get_random_string
from ..utils.generate_ai import generate_test


collection = get_collection('dashboard_teachers')
router = APIRouter()

# create a test 
@router.put('/test/create', status_code=201)
def test_create(username:str, info:dict):
    try:
        query_about = """Please generate some test question about {desc}. which have {mcq} questions of mcq, {short} questions of short answer and {long} questions of long answer. please give the response in json format and structure of like this:
        test = [{{ques="", opt=["a", "b", "c", "d"], ans="", mark=1}}, {{ques="", opt=[], ans=" ", mark=3}}]""".format(desc=info['desc'], mcq=info['mcq'], short=info['short'], long=info['long'])

        new_test = generate_test(query_about)
        
        dd_line = datetime.now()+ timedelta(days=7)   

        if info['title'] == '':
            info['title'] = 'No title'

        test_id = get_random_string()


        if 'status_code' in new_test and new_test['status_code']==200:
            sample_test = Test(
                test_id=test_id,
                title=info['title'],
                no_of_ques=info['mcq']+info['short']+info['long'],
                ques= new_test['test'],
                available=info['available'],
                time=info['time'],
                attempted=0,
                deadline = dd_line.isoformat(),
                created_at = datetime.utcnow().isoformat(),
                last_updated_at = datetime.utcnow().isoformat()
                )
            
            res = collection.update_one(
            {"username": username},
            {"$push": {"test":sample_test.dict()}}   
            )
        if res.modified_count==0:
            raise HTTPException(status_code=400, detail='Test creation failed')

        #  Distribute to students ( visiablity)

        available = info['available']
        if available:
            st_collec = get_collection('dashboard_students')
            for data in available:
                if data['subject']== "":
                    st_collec.update_many({'clg_roll': {'$gte': data['clg_roll'][0],'$lte': data['clg_roll'][1]}}, {"$push": {"test": { "id" : test_id, "username" : username}}})
                else :
                    st_collec.update_many({'course': data['course'], 'year': data['year'], "subjects" : data['subject'] }, {"$push": {"test": { "id" : test_id, "username" : username}}})



        return { "message" : "Test created successfully" , 'status_code' : 201}
    except Exception as e:
        raise HTTPException(status_code=400 , detail=str(e))

# Read/fetch all tests - by teacher       
@router.get('/test', status_code=200)
def all_test_get(username:str):
    try:
        res = collection.find_one({'username':username}, {'test' : 1})
        if not res:
            raise HTTPException(status_code=400, detail='Test not found')
        return { "message" : "Test found successfully" , 'status_code' : 200 , 'data' : dumps(res)}
    except Exception as e:
        raise HTTPException(status_code=400 , detail=str(e))

# delete a test - by teacher
@router.put('/test/delete', status_code=200)
def test_delete(username:str, test_id:str):
    try:
        
        res = collection.update_one(
        {"username": username},  
        {"$pull": {"test": {"test_id": test_id}}}   
        )
        if res.modified_count == 0:
            raise HTTPException(status_code=404, detail="Test not found")

        return { "message" : "Test deleted successfully" , 'status_code' : 201}
    except Exception as e:
        raise HTTPException(status_code=400 , detail=str(e))


#updat a test - by teacher
@router.put('/test/update', status_code=200)
def test_update(username:str, test_id:str, update_data:dict):
    try:
        update_query = {f"test.$.{key}": value for key, value in update_data.items()}

        # Perform the update
        result = collection.update_one(
            {"username": username, "test.test_id": test_id},  # Match condition
            {"$set": update_query}  # Dynamically set fields
        )

        # Check the result
        if result.modified_count > 0:
            return{ "message" : f"Test with test_id '{test_id}' updated successfully!", "status_code" : 200}
        else:
            return { "message" :f"No matching test found for test_id '{test_id}'." , "status_code" : 404}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



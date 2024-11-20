from fastapi import APIRouter, HTTPException

from ..utils.generate_ai import generate_content
# from ..db_connection import get_collection

router = APIRouter()


@router.post('/student/ask')
def ask_question(question:str, clg_roll:int):
    try:
        content = generate_content(question)
        # collection = get_collection('dashboard_students')
        return { "message" : "Content generate successfully", "status_code" : 200, "content" : content}
    except Exception as e:
        pass
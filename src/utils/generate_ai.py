import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=api_key)


def generate_test(query_about):
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query_about)
       
        if response._done == False :
                raise Exception("test generation failed")
        else :
            content = response.text 
            content = content[7: len(content)-5]
            try:
                response_dict = json.loads(content)
                return { 'message' : 'Test generated successfully', 'status_code' : 200, 'test' : response_dict['test']}
            except json.JSONDecodeError as e:
                raise Exception(str(e))
    except Exception as e:
        print(str(e))
        raise Exception(str(e))


def generate_content(query_about):
   
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query_about)
       
        if response._done == False :
                raise Exception("test generation failed")
        else :
           return { "message" : "Content generate successfully", "status_code" : 200, "content" : response.text}
    except Exception as e:
        raise Exception(str(e))



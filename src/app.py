from dotenv import load_dotenv
from db_connection import db_connection
from fastapi import FastAPI

# Load environment variables from .env file
load_dotenv()
app = FastAPI()

if __name__ == '__main__':
    db_connection()


@app.get('/')
def hello():
    return "hello world"


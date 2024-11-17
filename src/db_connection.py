import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# Retrieve MongoDB URI and database name from environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")


def db_connection():
   try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print('Successfully connected to MongoDB')
    return db
   except:
    print('Could not connect to MongoDB')
    return None


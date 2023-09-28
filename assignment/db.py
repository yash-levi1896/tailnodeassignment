from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_database():
    try:
        client = MongoClient(os.environ.get('MongoURL'))
        return client
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return None
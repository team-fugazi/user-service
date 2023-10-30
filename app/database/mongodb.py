from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

# access environment variables
db_protocol = os.getenv("DB_PROTOCOL")
db_user = os.getenv("DB_USERNAME")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_params = os.getenv("DB_QUERY_PARAMS")



# Database connection
db_uri = f"{db_protocol}://{db_user}:{db_pass}@{db_host}/?{db_params}"
client = MongoClient(db_uri)
database = client.services
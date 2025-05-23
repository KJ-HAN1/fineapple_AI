from dotenv import load_dotenv
import os

load_dotenv()

# db
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# els
ES_HOST = os.getenv("ES_HOST")
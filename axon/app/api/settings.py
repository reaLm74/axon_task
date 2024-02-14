import os

from dotenv import load_dotenv

load_dotenv()

driver = os.getenv('DRIVER')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')

DATABASE_URL = f"{driver}://{user}:{password}@{host}:{port}/{db_name}"

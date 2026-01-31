import os
from dotenv import load_dotenv

load_dotenv()

# Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
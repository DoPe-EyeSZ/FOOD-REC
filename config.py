import os
from dotenv import load_dotenv

load_dotenv()

# Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# PostgreSQL
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")

#TEST and PROD db
POSTGRES_DB_TEST=os.getenv("POSTGRES_DB_TEST")
POSTGRES_DB_PROD=os.getenv("POSTGRES_DB_PROD")

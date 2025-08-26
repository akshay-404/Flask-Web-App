import os
from dotenv import load_dotenv
load_dotenv("/home/ubuntu/Flask-Web-App/.env")

DB_USER = os.getenv("RDS_USER")
DB_PASS = os.getenv("RDS_PASSWORD")
DB_HOST = os.getenv("RDS_HOST")
DB_NAME = os.getenv("RDS_DBNAME")
DB_PORT = os.getenv("RDS_PORT", 3306)

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

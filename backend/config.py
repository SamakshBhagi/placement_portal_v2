import os
DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_EXPIRATION_SECONDS = 3000
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///" + os.path.join(INSTANCE_DIR, "placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

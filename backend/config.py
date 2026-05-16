import os
DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    #SECRET_KEY = "abcd12345"
    JWT_EXPIRATION_SECONDS = 3000
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///" + os.path.join(DIR, "instance","placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #EMAIL_USER = "samaksh.bhagi.dev@gmail.com"
    #EMAIL_PASSWORD = "xowumjoywlvqmhtz"

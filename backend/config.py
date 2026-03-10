import os
DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = "abcd12345"
    JWT_EXPIRATION_SECONDS = 3000
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DIR, "instance","placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_USER = "samaksh.bhagi.dev@gmail.com"
    EMAIL_PASSWORD = "xowumjoywlvqmhtz"
import os

class Config:
    DEBUG = False
    ABSOLUTE_URL='http://127.0.0.1:5000'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///products.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
import os 

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "DEV-SECRET-KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
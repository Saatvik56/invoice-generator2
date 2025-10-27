import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-this-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'

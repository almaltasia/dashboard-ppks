import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-ppks-key-change-in-production'
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123@localhost:5432/db_ppks'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    
    # Flask-Security settings
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'ppks-salt-change-in-production'
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-ppks-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
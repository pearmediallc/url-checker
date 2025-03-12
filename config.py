import os

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Server configuration
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 8000       # Production port
    
    # Application configuration
    DEBUG = False
    TESTING = False

import os

class Config:
    # Cambiar DATABASE_URL por el nombre de tu base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:@localhost/db_biblioteca')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    WTF_CSRF_ENABLED = True
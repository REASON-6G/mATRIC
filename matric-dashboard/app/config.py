import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x0c\x11\x1f\xe4\xd0@\xcc\x1b\x1bX}\x18\x03\xcc\x00\xcb\x93\xc2u\xe5\x06K^\x1a'
    DBHOST: str = os.getenv("DB_HOST","127.0.0.1")
    DBPORT: str = os.getenv("DB_PORT","5432")
    DBUSER: str = os.getenv("DB_USER","matricuser")
    DBPASSWORD: str = os.getenv("DB_PASSWORD","matricpassword")
    DBNAME: str = os.getenv("DB_NAME","matricdash")
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    UPLOAD_FOLDER = "uploads"

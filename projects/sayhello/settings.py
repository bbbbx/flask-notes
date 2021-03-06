import os
import sys
from sayhello import app

# 兼容不同系统 SQLite 的 URI
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.sqlite3')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

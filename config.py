import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'theatlantic'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'atlantic.db')
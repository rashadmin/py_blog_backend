import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    POSTS_PER_PAGE = 3
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'randomstring'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(basedir,"app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


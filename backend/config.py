import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testpass'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'convidhelper.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_FOLDER = os.path.join(basedir, 'app/ai_models/temp/')
    IP = "3.22.176.142"
    API_PORT = "5000"
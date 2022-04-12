import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
     # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'never-will-u-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db'
    )
    REDISTOGO_URL = os.environ.get('REDISTOGO_URL') or 'redis://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
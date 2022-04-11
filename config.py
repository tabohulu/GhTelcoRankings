import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    CONSUMER_KEY=os.environ.get('CONSUMER_KEY') or 'VTCECAvx0ki4yM6TsteJ6scUg'
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or "Aiq9QNn8qfEPiCNWEStuXai3ne1aI9glg0QA3DE3eE6Ce9iOpT"
    API_BEARER_TOKEN =  os.environ.get('API_BEARER_TOKEN') or "AAAAAAAAAAAAAAAAAAAAALu7bAEAAAAAcmdRO2I14fdkxlsBbYr69%2F9Jhvs%3Dpz7HnxcPiHVBWKzDDqA56A2cqz4cIvTw9kcwYjDs6F5Ak5ulqA"
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') or "1511553865602461700-oufEwXWifun0facSAibo8CkL8Xpwd5"
    ACCESS_SECRET = os.environ.get('ACCESS_SECRET') or "crly8KC3vz2NeSzQcqnIMAbJ0oqTuQkAyV1nKr1ThtknT"


     # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
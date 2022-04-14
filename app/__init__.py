from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app= Flask(__name__)
app.config.from_object(Config)
login =LoginManager(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
from app import routes,models

def create_admin(username,password,email):
    User = models.User
    if User.query.filter(User.username==username,User.user_type=='admin').first() is None:
        user=User(username=username,email=email,user_type='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'user created'
    return 'user already exists'    



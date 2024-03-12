# models.py

from flask_login import UserMixin
from .import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Subject(UserMixin,db.Model):
    sub_name = db.Column(db.String(100),primary_key=True)
    sub_code = db.Column(db.Integer,primary_key=True)
    teacher = db.Column(db.String(100))

class files(UserMixin,db.Model):
    id = db.Column("file_id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))


    def __init__(self, name, url):
        self.name = name
        self.url = url
        # self.created_date = datetime.datetime.now()

# class Books(UserMixin,db.Model):


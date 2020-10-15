from datetime import datetime
from career_guide import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return userr.query.get(int(user_id))


class userr(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    password=db.Column(db.String(80), nullable=False)
    dob= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender= db.Column(db.String(80), nullable=False)
    ambition=db.Column(db.String(50), nullable=False)
    qualification=db.Column(db.String(60), nullable=False)
    proimg = db.Column(db.String(20), nullable=False, default='download.png')

class field(db.Model):
    fieldname=db.Column(db.String(20), primary_key=True)
    reference=db.Column(db.Text, nullable=True)
    quote=db.Column(db.Text, nullable=True)
    quter=db.Column(db.Text, nullable=True)


class exam(db.Model):
    examname=db.Column(db.String(50), primary_key=True)
    offisite=db.Column(db.String(80), nullable=True)
    reference=db.Column(db.String(80), nullable=True)
    examdate=db.Column(db.DateTime, nullable=True)
    regidate=db.Column(db.DateTime, nullable=True)
    country=db.Column(db.String(20), nullable=True)
    agelimit=db.Column(db.String(20), nullable=True)
    noattempts=db.Column(db.Integer, nullable=True)
    fieldname=db.Column(db.String(60), nullable=True)
    after=db.Column(db.String(30), nullable=True)


class course(db.Model):
    coursename=db.Column(db.String(80), primary_key=True)
    reference=db.Column(db.Text, nullable=True)
    examname=db.Column(db.String(50), nullable=True)


class college(db.Model):
    collegename=db.Column(db.String(80), primary_key=True)
    coursename=db.Column(db.String(80), nullable=True)
    





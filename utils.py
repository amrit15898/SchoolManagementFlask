from flask import session
from models import db, Teachers, Subjects

def get_user():
    email = session["email"]
    user = Teachers.query.filter_by(email=email).first()
    return user
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime


db = SQLAlchemy()

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    password = db.Column(db.String(100))
    is_principal = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, name, subject_id):
        self.name = name
        self.email = email
        self.subject_id = subject_id
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(('utf-8'))

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)

class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    period_no = db.Column(db.Integer)
    teacher = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    subject = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))
    

class Attendence(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    is_present = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)






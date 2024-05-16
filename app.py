from flask import Flask, jsonify, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Teachers, Subjects, Attendence, TimeTable, Classes
from flask_migrate import Migrate
from utils import get_user
from datetime import datetime, date
from sqlalchemy import not_
from middlewares import auth, guest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amritpal:123456@localhost:5432/flask_db'
app.config['SECRET_KEY'] = 'amritpalsingh'
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
@guest
def register():
    subjects = Subjects.query.all()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        password = request.form["password"]

        new_user = Teachers(name=name, email=email, password=password, subject_id=subject)
        db.session.add(new_user)
        db.session.commit()
        return redirect("login-page")
    return render_template("home.html", subjects=subjects)


@app.route("/login-page", methods=["GET", "POST"])
@guest
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = Teachers.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["name"] = user.name
            session["email"] = user.email
            session["password"] = user.password
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid user")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
@auth
def dashboard():
    user = get_user()
    if True == user.is_principal:
        return redirect("/principal-panel")
    if request.method == "POST":
        punch_in = request.form["punch_in"]
        obj = Attendence(teacher=user.id, is_present=True)
        db.session.add(obj)
        db.session.commit()

    today = date.today()
    attendence_obj = Attendence.query.filter_by(teacher=user.id).filter(Attendence.created_at>=today).first()

    if attendence_obj is not None:
        today_present = attendence_obj.is_present
    else:
        today_present = False
    return render_template("dashboard.html", name=user, today_present=today_present)


@app.route("/logout")
def logout():
    session.pop("name", None)
    return render_template("login.html")


@app.route("/principal-panel")
def principal_panel():
    teachers = db.session.query(Teachers, Subjects).join(Subjects).all()
    teachers_attendance = {}
    today = date.today()
    print(f"today date is {today}")

    for teacher, subject in teachers:
        today_date = today.strftime('%Y-%m-%d')
        print(today_date)
        attendance = Attendence.query.filter_by(teacher=teacher.id).filter(db.func.date(Attendence.created_at) == today_date).first()
        teachers_attendance[teacher.id] = attendance

    return render_template("principal_panel.html", teachers=teachers, teacher_attendance=teachers_attendance)

@app.route('/get-teachers')
def get_absent_teachers():
    today_date = date.today()

    query = db.session.query(
        Teachers, Subjects
    ).join(Subjects, Teachers.subject_id == Subjects.id)
    print(query.all())
    latest_attendance = db.session.query(
        Attendence.teacher, db.func.max(Attendence.created_at).label("latest_date")
    ).filter(db.func.date(Attendence.created_at) == today_date).group_by(Attendence.teacher).all()

    teachers_without_attendance = []

    for teacher, subject in query.all():
        has_attendance_today = False

        for att_teacher, latest_date in latest_attendance:
            if att_teacher == teacher.id:
                has_attendance_today = True
                break

        if not has_attendance_today:
            teachers_without_attendance.append((teacher, subject))

    for teacher, subject in teachers_without_attendance:
        print("Teacher ID:", teacher.id, "Name:", teacher.name, "Subject:", subject.name)

    return render_template("absent-teachers.html", teachers_without_attendance=teachers_without_attendance)


@app.route("/get-class/<int:id>")
def get_absent_teacher_classes(id):
    time_tables_with_details = db.session.query(
        TimeTable,
        Subjects,
        Teachers,
        Classes
    ).join(
        Teachers, TimeTable.teacher == Teachers.id
    ).join(
        Subjects, TimeTable.subject == Subjects.id
    ).join(
        Classes, TimeTable.class_id == Classes.id
    ).all()
    period_no = 1

    free_teachers = Teachers.query.filter(
        not_(Teachers.id.in_(
            TimeTable.query.with_entities(TimeTable.teacher)
                    .filter(TimeTable.period_no == period_no)
        ))
    ).all()
    free_teachers_objs = [{
        "name": teacher.name,
        "email": teacher.email
    } for teacher in free_teachers]
    print(free_teachers_objs)

    return render_template("free-classess.html", objs = time_tables_with_details)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Blueprint, render_template
from .db import get_db

indexBp = Blueprint("index", __name__)
blogBP = Blueprint("blog", __name__, url_prefix="/blog")

@indexBp.route("/")
def landing_page():
    return render_template("index.html")

@blogBP.route("/students")
def students_page():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()

    return render_template("students.html", rows=students)

@blogBP.route("/teachers")
def teachers_page():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM teachers")
        teachers = cur.fetchall()
    return render_template("teachers.html", rows=teachers)

@blogBP.route("/grades")
def grades_page():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM grades")
        grades = cur.fetchall()

    return render_template("grades.html", rows=grades)

@blogBP.route("/api")
def api_page():
    return render_template("api.html")
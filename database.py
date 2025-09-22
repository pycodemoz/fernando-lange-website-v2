import os
from dotenv import load_dotenv
from flask import url_for
from sqlalchemy import create_engine, text


load_dotenv()

db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:senha@localhost:5432/courses_db")

engine = create_engine(db_url)


# Se estiver usando Render, força SSL
if "render.com" in db_url:
    if "?" in db_url:
        db_url += "&sslmode=require"
    else:
        db_url += "?sslmode=require"

engine = create_engine(db_url)

# engine = create_engine(
    #             "mysql+pymysql://root:Riqueza1822@localhost/courses")


def load_courses_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courses"))
        courses = []
        for row in result.mappings().all():
            course = dict(row)
            course["image_filename"] = course.get("image")  # apenas o nome do arquivo
            courses.append(course)
        return courses


def load_course_db_id(id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM courses WHERE id = :val"),
            {"val": id}
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        course = dict(rows[0]._mapping)
        course["image_filename"] = course.get("image")
        return course


def check_existing_subscription(course_id, email):
    with engine.connect() as conn:
        query = text("SELECT COUNT(*) as count FROM forms WHERE course_id = :course_id AND email = :email")
        result = conn.execute(query, {
            'course_id': course_id,
            'email': email
        })
        count = result.fetchone()[0]
        return count > 0 


def add_dataform_to_db(course_id, data):
    if check_existing_subscription(course_id, data['email']):
        raise ValueError("Este email já está inscrito neste curso.")
    with engine.connect() as conn:
        query = text("""
            INSERT INTO forms (course_id, full_name, phone, email, level_know)
            VALUES (:course_id, :full_name, :phone, :email, :level_know)
        """)
        conn.execute(query, {
            'course_id': course_id,
            'full_name': data['full_name'],
            'phone': data['phone'],  
            'email': data['email'],
            'level_know': data['level_know']  
        })
        conn.commit()
        
def view_students_db():
    with engine.connect() as conn:
        query = conn.execute(text("SELECT * FROM forms"))
        students = []
        for row in query.mappings().all():
            students.append(dict(row)) 
        return students



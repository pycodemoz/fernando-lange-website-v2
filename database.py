import os
from flask import url_for
from sqlalchemy import create_engine, text



# Pega a connection string do Render
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise ValueError("A variável de ambiente DATABASE_URL não está definida.")

engine = create_engine(db_url)

print("DATABASE_URL:", db_url)



# engine = create_engine(
    #             "mysql+pymysql://root:Riqueza1822@localhost/courses")


def load_courses_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courses"))
        courses = []
        for row in result.mappings().all():
            course = dict(row)

            # Gera a URL completa do arquivo estático
            if course.get("image"):
                course["image_url"] = url_for("static", filename=course["image"])
            else:
                course["image_url"] = None  # opcional: pode colocar url_for("static", filename="no_image.png")

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
        else:
           return dict(rows[0]._mapping)
       
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
    
    with engine.begin() as conn:  # ← begin() garante commit automático
        query = text("""
            INSERT INTO forms (course_id, full_name, phone, email, level_know)
            VALUES(:course_id, :full_name, :phone, :email, :level_know)
        """)
        conn.execute(query, {
            'course_id': course_id,
            'full_name': data['full_name'],
            'phone': data['phone'],  
            'email': data['email'],
            'level_know': data['level_know']  
        })




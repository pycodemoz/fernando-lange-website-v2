from flask import Flask, render_template, jsonify, request
from database import load_courses_db, load_course_db_id, add_dataform_to_db, view_students_db



app = Flask(__name__)

# Rotas Flask
@app.route("/")
def home():
    courses = load_courses_db()
    return render_template("home.html", courses=courses)

@app.route("/api/courses/")
def list_courses():
    return jsonify(load_courses_db())

@app.route("/course/<int:id>")
def show_course(id):
    course = load_course_db_id(id)
    if not course:
        return jsonify({"error": "Curso não encontrado"}), 404
    return jsonify(course)

@app.route("/subscribe/<int:id>")
def subscribe_course(id):
    course = load_course_db_id(id)
    if not course:
        return "Curso não encontrado", 404
    return render_template("form.html", course=course)

@app.route("/course/<int:id>/submit", methods=["POST"])
def submit_course(id):
    data = request.form.to_dict()
    selected_course = load_course_db_id(id)
    
    if not selected_course:
        return "Curso não encontrado.", 404

    try:
        add_dataform_to_db(id, data)
        return render_template("form_submited.html", submit=data, course=selected_course)
    except ValueError as e:
        return render_template("form.html", course=selected_course, error=str(e))
    except Exception as e:
        return f"Erro inesperado: {e}"

@app.route("/api/students/list")
def students_list():
    return jsonify(view_students_db())

@app.route("/students/subscribe")
def students_subcribe():
    students = view_students_db()  # carrega students com course_id
    courses = load_courses_db()    # carrega courses com id e title
    
    # Faz o "join" manual
    for student in students:
        course_id = student.get('course_id')
        if course_id:
            # Encontra o curso pelo ID
            course = next((c for c in courses if c['id'] == course_id), None)
            student['course_title'] = course['title'] if course else 'Curso não encontrado'
        else:
            student['course_title'] = 'Não inscrito'
    
    return render_template("students.html", students=students)
    
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
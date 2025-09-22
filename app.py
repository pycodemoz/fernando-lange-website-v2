from flask import Flask, render_template, jsonify, request
from database import load_courses_db, load_course_db_id, add_dataform_to_db



app = Flask(__name__)

    
@app.route("/")
def home():
    courses = load_courses_db()
    return render_template('home.html', courses=courses)

@app.route("/api/courses/")
def list_course():
    return jsonify(load_courses_db())

@app.route("/course/<id>")
def show_course(id):
    course = load_course_db_id(id)
    return(jsonify(course))


@app.route("/subscribe/<int:id>")
def subscribe_course(id):
    courses = load_courses_db()
    # Busca o curso pelo ID
    selected_course = next((c for c in courses if c["id"] == id), None)

    if not selected_course:
        return "Curso não encontrado.", 404

    # Renderiza o formulário com os dados do curso
    return render_template("form.html", course=selected_course)




@app.route("/course/<id>/submit", methods=["POST"])
def submit_course(id):
    courses = load_courses_db()
    data = request.form.to_dict()
    data['course_id'] = id
    selected_course = None
    for c in courses:
        if str(c["id"]) == str(id):
            selected_course = c
            break
    
    try:
        add_dataform_to_db(id, data)
        return render_template('form_submited.html', submit=data, course=selected_course)
    except ValueError as e:
        # Renderizar o formulário novamente com mensagem de erro
        return render_template('form.html', course=selected_course, error=str(e))
    

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
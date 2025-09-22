from flask import Flask, render_template, jsonify, request
from database import load_courses_db, load_course_db_id, add_dataform_to_db, engine



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


# Teste de conexão com DB

@app.route("/test-db")
def test_db():
    try:
        result = engine.execute("SELECT 1").fetchall()
        return f"DB conectado: {result}"
    except Exception as e:
        return f"Erro DB: {e}"
    

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
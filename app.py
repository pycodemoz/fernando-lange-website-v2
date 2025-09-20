from flask import Flask, render_template, jsonify
from sqlalchemy import text
from database import engine



app = Flask(__name__)


def load_courses_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courses"))
        courses = []
        for row in result.mappings().all():   # <-- .mappings() transforma em dict
            courses.append(dict(row))
        return courses

        
@app.route("/")
def home():
    courses = load_courses_db()
    return render_template('home.html', courses=courses)

@app.route("/api/courses/")
def list_course():
    return jsonify(load_courses_db())

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
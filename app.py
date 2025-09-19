from flask import Flask, render_template, jsonify


app = Flask(__name__)


COURSES = [
    {
        'id': 1,
        'title': "Curso de HTML e CSS",
        'image': "static/html_css.jpeg"
    },
    {
        'id': 2,
        'title': "Curso de JavaScript",
        'image': "static/js.png"
    },
    {
        'id': 3,
        'title': "Curso de Python",
        'image': "static/python.jpeg"
    },
    {
        'id': 4,
        'title': "Curso de Django",
        'image': "static/django.jpeg"
    },
    
    {
        'id': 5,
        'title': "Curso de Django Rest Framework",
        'image': "static/rest_framework.png"
    }
]


@app.route("/")
def home():
  return render_template('home.html', courses=COURSES)

@app.route("/api/courses/")
def list_course():
    return jsonify(COURSES)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
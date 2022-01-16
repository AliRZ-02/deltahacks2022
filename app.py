from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from data_models import Course

# Creating the Flask App and Configuring the Database through SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///requests.db'
db = SQLAlchemy(app)

# Class that handles the database and the columns present in it
class UserIN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(200), nullable=False)
    course_1 = db.Column(db.String(200), nullable=True)
    course_2 = db.Column(db.String(200), nullable=True)
    course_3 = db.Column(db.String(200), nullable=True)
    course_4 = db.Column(db.String(200), nullable=True)
    course_5 = db.Column(db.String(200), nullable=True)
    course_6 = db.Column(db.String(200), nullable=True)
    coop = db.Column(db.Boolean, nullable=False)
    ap = db.Column(db.Boolean, nullable=False)
    ib = db.Column(db.Boolean, nullable=False)
    ecs = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id


# Main Website URL - Uses index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uni = request.form.get('school', 'McMaster University')
        program = request.form.get('program', 'Arts & Science')
        course_1 = Course(request.form.get('course_1', 'ATC4M'), int(request.form.get('course_1_grade', 80)))
        course_2 = Course(request.form.get('course_2', 'ATC4M'), int(request.form.get('course_2_grade', 80)))
        course_3 = Course(request.form.get('course_3', 'ATC4M'), int(request.form.get('course_3_grade', 80)))
        course_4 = Course(request.form.get('course_4', 'ATC4M'), int(request.form.get('course_4_grade', 80)))
        course_5 = Course(request.form.get('course_5', 'ATC4M'), int(request.form.get('course_5_grade', 80)))
        course_6 = Course(request.form.get('course_6', 'ATC4M'), int(request.form.get('course_6_grade', 80)))
        ecs = [ec.strip() for ec in request.form.get('extra_curriculars', '').split(',')]
        ib = True if request.form.get('ib') == 'YES' else False
        ap = True if request.form.get('ap') == 'YES' else False
        coop = True if request.form.get('coop') == 'YES' else False


    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def about():
    return index()


@app.route('/addReview', methods=['GET', 'POST'])
def add_review():
    return render_template('reviews.html')


if __name__ == "__main__":
    app.run(debug=True)

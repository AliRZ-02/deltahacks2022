import os
import pathlib
from datetime import datetime

from flask import Flask, render_template, request, redirect
from difflib import get_close_matches
from flask_sqlalchemy import SQLAlchemy
from data_models import Course, UserData
from chances import parse_user_info, get_missing_courses, get_ec_level
from typing import List

# Creating the Flask App and Configuring the Database through SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///requests.db'
db = SQLAlchemy(app)


class UserReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    uni = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(200), nullable=False)
    course_1 = db.Column(db.String(200), nullable=False)
    course_2 = db.Column(db.String(200), nullable=False)
    course_3 = db.Column(db.String(200), nullable=False)
    course_4 = db.Column(db.String(200), nullable=False)
    course_5 = db.Column(db.String(200), nullable=False)
    course_6 = db.Column(db.String(200), nullable=False)
    course_1_g = db.Column(db.String(200), nullable=False)
    course_2_g = db.Column(db.String(200), nullable=False)
    course_3_g = db.Column(db.String(200), nullable=False)
    course_4_g = db.Column(db.String(200), nullable=False)
    course_5_g = db.Column(db.String(200), nullable=False)
    course_6_g = db.Column(db.String(200), nullable=False)
    coop = db.Column(db.Boolean, nullable=False)
    ap = db.Column(db.Boolean, nullable=False)
    ib = db.Column(db.Boolean, nullable=False)
    ec_level = db.Column(db.Text, nullable=True)
    accepted = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class UserOUT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(200), nullable=False)
    course_1 = db.Column(db.String(200), nullable=False)
    course_2 = db.Column(db.String(200), nullable=False)
    course_3 = db.Column(db.String(200), nullable=False)
    course_4 = db.Column(db.String(200), nullable=False)
    course_5 = db.Column(db.String(200), nullable=False)
    course_6 = db.Column(db.String(200), nullable=False)
    course_1_g = db.Column(db.String(200), nullable=False)
    course_2_g = db.Column(db.String(200), nullable=False)
    course_3_g = db.Column(db.String(200), nullable=False)
    course_4_g = db.Column(db.String(200), nullable=False)
    course_5_g = db.Column(db.String(200), nullable=False)
    course_6_g = db.Column(db.String(200), nullable=False)
    coop = db.Column(db.Boolean, nullable=False)
    ap = db.Column(db.Boolean, nullable=False)
    ib = db.Column(db.Boolean, nullable=False)
    ecs = db.Column(db.Text, nullable=True)
    chance = db.Column(db.String, nullable=False)
    missing_courses = db.Column(db.String, nullable=True)
    ec_level = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


def get_program_list() -> List[str]:
    path = pathlib.Path('programs')
    files = os.listdir(f'{path}')
    return [file.split('.json')[0].strip() for file in files]


def reduce_db():
    users = UserOUT.query.order_by(UserOUT.date_created).all()
    for user in users:
        db.session.delete(user)
        db.session.commit()


def remove_consecutive_duplicates(s):
    if len(s)<2:
        return s
    if s[0] == '_' and s[0]==s[1]:
        return remove_consecutive_duplicates(s[1:])
    else:
        return s[0]+remove_consecutive_duplicates(s[1:])


def legal_name(name: str) -> str:
    valids = list("abcdefghijklmnopqrstuvwxyz1234567890")
    name_to_return = []
    for char in name:
        if char in valids:
            name_to_return.append(char)
        else:
            name_to_return.append('_')

    name = "".join(name_to_return)
    return remove_consecutive_duplicates(name)


# Main Website URL - Uses index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uni = request.form.get('school', 'McMaster University')
        given_program = request.form.get('program', 'Arts & Science')
        program = legal_name(given_program.lower())
        programs = get_program_list()
        closest_program = str(get_close_matches(program, programs, n=5)[0])
        course_1 = Course(request.form.get('course_1', 'NONE'), int("80" if request.form.get('course_1_grade', 80) is "" else request.form.get('course_1_grade', 80)))
        course_2 = Course(request.form.get('course_2', 'NONE'), int("80" if request.form.get('course_2_grade', 80) is "" else request.form.get('course_2_grade', 80)))
        course_3 = Course(request.form.get('course_3', 'NONE'), int("80" if request.form.get('course_3_grade', 80) is "" else request.form.get('course_3_grade', 80)))
        course_4 = Course(request.form.get('course_4', 'NONE'), int("80" if request.form.get('course_4_grade', 80) is "" else request.form.get('course_4_grade', 80)))
        course_5 = Course(request.form.get('course_5', 'NONE'), int("80" if request.form.get('course_5_grade', 80) is "" else request.form.get('course_5_grade', 80)))
        course_6 = Course(request.form.get('course_6', 'NONE'), int("80" if request.form.get('course_6_grade', 80) is "" else request.form.get('course_6_grade', 80)))
        courses = [course_1, course_2, course_3, course_4, course_5, course_6]
        non_empty_courses = [course for course in courses if course.name != 'NONE']
        ecs = [ec.strip() for ec in request.form.get('extra_curriculars', '').split(',')]
        ib = True if request.form.get('ib') == 'YES' else False
        ap = True if request.form.get('ap') == 'YES' else False
        coop = True if request.form.get('coop') == 'YES' else False
        data = UserData(non_empty_courses, ecs, coop, closest_program, ap, ib)
        user_chances = parse_user_info(data)
        missing_courses = get_missing_courses(data.program_of_choice, data.courses)
        if len(missing_courses) > 6:
            missing_courses = missing_courses[:6]
        if len(missing_courses) == 0: missing_courses = ['NONE']
        ec_level = get_ec_level(data.extra_curriculars)
        course_1_name = course_1.name if course_1.name != 'NONE' else 'N/A'
        course_1_grade = course_1.grade if course_1_name != 'N/A' else 0
        course_2_name = course_2.name if course_2.name != 'NONE' else 'N/A'
        course_2_grade = course_2.grade if course_2_name != 'N/A' else 0
        course_3_name = course_3.name if course_3.name != 'NONE' else 'N/A'
        course_3_grade = course_3.grade if course_3_name != 'N/A' else 0
        course_4_name = course_4.name if course_4.name != 'NONE' else 'N/A'
        course_4_grade = course_4.grade if course_4_name != 'N/A' else 0
        course_5_name = course_5.name if course_5.name != 'NONE' else 'N/A'
        course_5_grade = course_5.grade if course_5_name != 'N/A' else 0
        course_6_name = course_6.name if course_6.name != 'NONE' else 'N/A'
        course_6_grade = course_6.grade if course_6_name != 'N/A' else 0
        returnData = UserOUT(uni=uni, program=given_program, course_1=course_1_name, course_1_g=course_1_grade, course_2=course_2_name,
                             course_2_g=course_2_grade, course_3=course_3_name, course_3_g=course_3_grade,
                             course_4=course_4_name, course_4_g=course_4_grade, course_5=course_5_name,
                             course_5_g=course_5_grade, course_6=course_6_name, course_6_g=course_6_grade,
                             coop=coop, ap=ap, ib=ib, ecs=", ".join(ecs),
                             chance=user_chances, missing_courses=", ".join(missing_courses), ec_level=ec_level)
        db.session.add(returnData)
        db.session.commit()
        return redirect('/results')
    else:
        userouts = UserOUT.query.order_by(UserOUT.date_created.desc()).all()
        return render_template('index.html', userouts=userouts)


@app.route('/results', methods=['GET', 'POST'])
def about():
    return index()


@app.route('/reviews', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        print('HERE')
        name = request.form.get('name', 'User')
        uni = request.form.get('school', 'McMaster University')
        given_program = request.form.get('program', 'Arts & Science')
        program = legal_name(given_program.lower())
        programs = get_program_list()
        closest_program = str(get_close_matches(program, programs, n=5)[0])
        course_1 = Course(request.form.get('course_1', 'NONE'),
                          int("80" if request.form.get('course_1_grade', 80) is "" else request.form.get('course_1_grade', 80)))
        course_2 = Course(request.form.get('course_2', 'NONE'),
                          int("80" if request.form.get('course_2_grade', 80) is "" else request.form.get('course_2_grade', 80)))
        course_3 = Course(request.form.get('course_3', 'NONE'),
                          int("80" if request.form.get('course_3_grade', 80) is "" else request.form.get('course_3_grade', 80)))
        course_4 = Course(request.form.get('course_4', 'NONE'),
                          int("80" if request.form.get('course_4_grade', 80) is "" else request.form.get('course_4_grade', 80)))
        course_5 = Course(request.form.get('course_5', 'NONE'),
                          int("80" if request.form.get('course_5_grade', 80) is "" else request.form.get('course_5_grade', 80)))
        course_6 = Course(request.form.get('course_6', 'NONE'),
                          int("80" if request.form.get('course_6_grade', 80) is "" else request.form.get('course_6_grade', 80)))
        courses = [course_1, course_2, course_3, course_4, course_5, course_6]
        non_empty_courses = [course for course in courses if course.name != 'NONE']
        ecs = [ec.strip() for ec in request.form.get('extra_curriculars', '').split(',')]
        ib = True if request.form.get('ib') == 'YES' else False
        ap = True if request.form.get('ap') == 'YES' else False
        coop = True if request.form.get('coop') == 'YES' else False
        accepted = True if request.form.get('coop') == 'YES' else False
        data = UserData(non_empty_courses, ecs, coop, closest_program, ap, ib)
        ec_level = get_ec_level(data.extra_curriculars)
        course_1_name = course_1.name if course_1.name != 'NONE' else 'N/A'
        course_1_grade = course_1.grade if course_1_name != 'N/A' else 0
        course_2_name = course_2.name if course_2.name != 'NONE' else 'N/A'
        course_2_grade = course_2.grade if course_2_name != 'N/A' else 0
        course_3_name = course_3.name if course_3.name != 'NONE' else 'N/A'
        course_3_grade = course_3.grade if course_3_name != 'N/A' else 0
        course_4_name = course_4.name if course_4.name != 'NONE' else 'N/A'
        course_4_grade = course_4.grade if course_4_name != 'N/A' else 0
        course_5_name = course_5.name if course_5.name != 'NONE' else 'N/A'
        course_5_grade = course_5.grade if course_5_name != 'N/A' else 0
        course_6_name = course_6.name if course_6.name != 'NONE' else 'N/A'
        course_6_grade = course_6.grade if course_6_name != 'N/A' else 0
        returnData = UserReviews(name=name, uni=uni, program=given_program, course_1=course_1_name, course_1_g=course_1_grade, course_2=course_2_name,
                             course_2_g=course_2_grade, course_3=course_3_name, course_3_g=course_3_grade,
                             course_4=course_4_name, course_4_g=course_4_grade, course_5=course_5_name,
                             course_5_g=course_5_grade, course_6=course_6_name, course_6_g=course_6_grade,
                             coop=coop, ap=ap, ib=ib, accepted=accepted, ec_level=ec_level)
        db.session.add(returnData)
        db.session.commit()
        return redirect('/reviews/results')
    else:
        reviews = UserReviews.query.order_by(UserReviews.date_created.desc()).all()
        return render_template('reviews.html', reviews=reviews)


@app.route('/reviews/results', methods=['GET', 'POST'])
def see_review():
    return add_review()


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug=True)

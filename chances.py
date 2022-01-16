import json
import re
from typing import List

from data_models import Course, UserData


def parse_user_info(info: UserData):
    sum = 0
    total_score = 0

    with open(f'programs/{info.program_of_choice}.json') as f:
        req_data = json.loads(f.read())

    for i in info.courses:
        sum += i.grade

    avg = sum / len(info.courses) if len(info.courses) != 0 else 80
    admavg = get_admission_avg(req_data)
    dif = admavg - avg
    if dif > 7:
        total_score += 3
    elif 7 >= dif >= 3:
        total_score += 5
    elif 2 >= dif >= 0:
        total_score +=10
    elif 0 > dif >= -3:
        total_score += 12
    elif dif < -3:
        total_score += 15
    x = len(info.extra_curriculars)
    if 0 <= x <= 2:
        total_score += 2
    elif 3 <= x <= 5:
        total_score += 5
    elif x > 5:
        total_score += 7
    if info.is_ap is True or info.is_ib is True:
        total_score += 2
    if total_score >= 15:
        return "HIGH CHANCE"
    elif 15 > total_score >= 10:
        return "MEDIUM CHANCE"
    elif total_score < 10:
        return "LOW CHANCE"


def get_missing_courses(program: str, courses: List[Course]) -> List[str]:
    with open(f'programs/{program}.json') as f:
        json_text = json.loads(f.read())
        courses_needed = json_text.get('information').get('req_courses')

        req_courses = []
        for course in courses_needed:
            req_courses.extend(get_course_code(course))

        print(req_courses)

        missing_courses = []
        courses_taken = [course.name for course in courses]
        for course in req_courses:
            if course not in courses_taken:
                missing_courses.append(course)

        return missing_courses


def get_course_code(given_course: str) -> List[str]:
    return re.findall('[A-Z]{3}4[UCOM]', given_course)


def get_ec_level(ecs: List[str]) -> str:
    x = len(ecs)
    if 0 <= x <= 2: return 'LOW'
    elif 3 <= x <= 5: return 'DECENT'
    elif x > 5: return 'IMPRESSIVE'


def get_admission_avg(data):
    avgs = re.findall(r'\d{2}', data.get('information').get('admission_range'))
    avgs = [float(avg) for avg in avgs]
    return max(avgs)

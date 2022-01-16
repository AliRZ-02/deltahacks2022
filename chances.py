from data_models import Course, UserData, ReturnData, ScrapingData

def parse_user_info(info: UserData):
    sum = 0
    total_score = 0
    if info.courses != ScrapingData.req_courses:
        ReturnData.entrance_chance = "NO CHANCE"
        return ReturnData.entrance_chance
    for i in info.courses:
        sum += Course.grade
    avg = sum / len(info.courses)
    admavg = int(ScrapingData.admission_range.strip("min. %"))
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
    if 1 <= x <= 2:
        total_score += 2
    elif 3 <= x <= 5:
        total_score += 5
    elif x > 5:
        total_score += 7
    if info.is_ap == True or info.is_ib == True:
        total_score += 2
    if total_score >= 15:
        ReturnData.entrance_chance = "HIGH CHANCE"
        return ReturnData.entrance_chance
    elif 15 > total_score >= 10:
        ReturnData.entrance_chance = "MEDIUM CHANCE"
        return ReturnData.entrance_chance
    elif total_score < 10:
        ReturnData.entrance_chance = "LOW CHANCE"
        return ReturnData.entrance_chance
    
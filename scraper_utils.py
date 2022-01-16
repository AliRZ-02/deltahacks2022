import json
import pathlib
import re
import time
import bs4
import os
import data_models
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
GOOGLE_CHROME_PATH = os.environ.get('GOOGLE_CHROME_BIN')
CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                               chrome_options=chrome_options)


def get_program_info(url: str):
    browser.get(url)
    el = browser.find_element_by_id('student-status')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Attending / Recently Graduated from a Canadian Secondary School':
            option.click()  # select() in earlier versions of webdriver
            break
    el = browser.find_element_by_id('provinces')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Ontario':
            option.click()  # select() in earlier versions of webdriver
            break
    element = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located(
            (By.ID, 'submit'))
    )

    browser.execute_script("arguments[0].scrollIntoView();", element)

    element.click()
    browser.implicitly_wait(1)
    prog_info = browser.find_element_by_id('program-1').text
    prog_infos = prog_info.split('\n')
    # print(prog_infos)
    name = prog_infos[0].split('Program ')[1].strip()
    province = prog_infos[1].split('Province')[1].strip()
    ouac_code = prog_infos[2].split('OUAC Code: ')[1].strip()
    degrees = [degree.strip() for degree in
               prog_infos[3].split('Degrees ')[1].split(',')]
    coop_option = False if 'no' in prog_infos[4].split('Co-op/Internship: ')[
                               1].strip().lower() else True
    req_courses = browser.find_element_by_xpath(
        '//*[@id="program-1"]/table/tbody/tr[8]/td/ul[1]').text.strip().split(
        '\n')
    try:
        admission_range = browser.find_element_by_xpath(
        '//*[@id="program-1"]/table/tbody/tr[12]/td').text.strip()
    except:
        admission_range = browser.find_element_by_xpath(
            '//*[@id="program-1"]/table/tbody/tr[11]/td').text.strip()

    try:
        enrolment = int(re.findall(r'\d+', browser.find_element_by_xpath(
        '//*[@id="program-1"]/table/tbody/tr[16]/td').text.strip())[0])
    except:
        enrolment = int(re.findall(r'\d+', browser.find_element_by_xpath(
            '//*[@id="program-1"]/table/tbody/tr[15]/td').text.strip())[0])

    return data_models.ScrapingData(name, province,
                                             'McMaster University', ouac_code,
                                             degrees, coop_option, req_courses,
                                             admission_range,
                                             enrolment)


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


def fetch_programs(url: str):
    programs = requests.get(url).text
    soup = bs4.BeautifulSoup(programs, features="html.parser")
    program_divs = soup.find_all("div", {"class": "row row-eq-height center-content"})[0].find_all('div')

    programs = []
    for program_div in program_divs:
        try:
            time.sleep(1)
            programs.append(data_models.Program(
                program_div.find('a').text,
                program_div.find('a').get('href'),
                get_program_info(program_div.find('a').get('href'))
            ))
        except Exception as e:
            print(f'Error on website: {program_div.find("a").get("href")}')
    return programs


def mcmaster_programs():
    return fetch_programs('https://future.mcmaster.ca/programs/')


# progs = mcmaster_programs()

# for prog in progs:
#     output_file = f'programs/{legal_name(prog.name.lower())}_program.json'
#     with open(output_file, 'w') as outfile:
#         json.dump(prog.__dict__(), outfile)

path = pathlib.Path('programs')
files = os.listdir(path)
for file in files:
    os.rename(f'{path}/{file}', f'{path}/{file.replace("_program", "")}')

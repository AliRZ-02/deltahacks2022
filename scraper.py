import json
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

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)


def search_program(program: str):
    with open(f'programs/{program}') as f:
        text = f.read()
        return json.loads(text)['link']


def get_requirements(user_info: data_models.UserData):
    search_program(user_info.program_of_choice)

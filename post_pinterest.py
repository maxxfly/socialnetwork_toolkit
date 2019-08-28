# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from random import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy.sql.expression import func

import time
import requests
import datetime
import re
import logging
import shutil
import os
import argparse

from datetime import datetime
from lib.post import Post

dirpath = os.getcwd()

def login(driver, email, password):
    driver.get('https://www.pinterest.fr/')
    driver.find_elements_by_partial_link_text("Log in")[0].click()

    driver.find_element_by_name("id").send_keys(email)
    driver.find_element_by_name("password").send_keys(password)

    driver.find_elements_by_css_selector("[data-test-id=registerFormSubmitButton] > button")[0].click()
    time.sleep(15)

def add_picture(driver, path, message, board, url_target):
    driver.find_elements_by_css_selector(".addPinFooter")[0].click()
    driver.find_element_by_id("cancelInstallButton").click()

    driver.find_elements_by_css_selector(".addPinFooter")[0].click()
    driver.find_elements_by_css_selector("[data-test-id=createAPin] [role=button]")[0].click()

    time.sleep(2)

    driver.find_elements_by_tag_name("textarea")[1].send_keys(message)

    if url_target:
        driver.find_elements_by_tag_name("textarea")[2].send_keys(url_target)

    # upload img
    driver.find_element_by_id("media-upload-input").send_keys(path)

    # select board
    driver.find_elements_by_css_selector("[data-test-id=board-dropdown-select-button]")[0].click()
    time.sleep(2)
    driver.find_elements_by_css_selector("div[title=" + board + "]")[0].find_element_by_xpath('../..').click()

parser = argparse.ArgumentParser(description='Post picture on Pinterest')

parser.add_argument('--username', dest='username', action='store', required=True,
                      help='username for Pinterest')

parser.add_argument('--password', dest='password', action='store', required=True,
                      help='password for Pinterest')

parser.add_argument('--board', dest='board', action='store', required=True,
                      help='board to use on Pinterest')

parser.add_argument('--headless', dest='headless', action='store_true',
                      help='use headless=True for Firefox')

parser.add_argument('--simulate', dest='simulate', action='store_true',
                      help='don\'t post picture on Pinterest and modify flag in database'
                    )

args = parser.parse_args()

e = create_engine('sqlite:///data/file.db')
Session = sessionmaker(bind=e)
session = Session()

query = session.query(Post).filter(and_(Post.use_on_pinterest == False,
                                        func.length(Post.description) < 500)).order_by(Post.posted_at).first()

if(query and query.id):
    options = Options()
    options.headless = args.headless

    driver = webdriver.Firefox(options=options)

    login(driver, args.username, args.password)
    add_picture(driver, (dirpath + "/system/" + query.key + ".jpg"), query.description, args.board, query.url_target)
    time.sleep(10)

    if args.simulate == False:
        query.use_on_pinterest = True
        session.commit()
        driver.find_elements_by_css_selector('[data-test-id=board-dropdown-save-button]')[0].click()
        time.sleep(5)
        driver.close()

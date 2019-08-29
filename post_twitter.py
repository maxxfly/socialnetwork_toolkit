# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

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
    driver.get('https://twitter.com/login')
    username_field = driver.find_element_by_class_name("js-username-field")

    # enter your username:
    username_field.send_keys(email)
    driver.implicitly_wait(2)

    # enter your password:
    password_field = driver.find_elements_by_css_selector(".js-password-field")[0]
    password_field.click()
    password_field.send_keys(password)
    driver.implicitly_wait(2)

    driver.find_elements_by_css_selector("button.submit")[0].click()

def add_picture(driver, path, message, url_target):
    driver.get('https://twitter.com/compose/tweet')

    driver.implicitly_wait(3)
    time.sleep(3)

    el = driver.find_element_by_class_name('public-DraftEditor-content')
    el.send_keys(message)

    if url_target:
        el.send_keys(" 👉 " + url_target + " 🌎 ")

    #el.send_keys(Keys.ESCAPE)

    driver.find_elements_by_css_selector("input[type=file]")[0].send_keys(path)

parser = argparse.ArgumentParser(description='Post picture on Twitter')

parser.add_argument('--username', dest='username', action='store', required=True,
                      help='username for Twitter')

parser.add_argument('--password', dest='password', action='store', required=True,
                      help='password for Twitter')

parser.add_argument('--headless', dest='headless', action='store_true',
                      help='use headless=True for Firefox')

parser.add_argument('--simulate', dest='simulate', action='store_true',
                      help='don\'t post picture on Twitter and modify flag in database'
                    )

args = parser.parse_args()

e = create_engine('sqlite:///data/file.db')
Session = sessionmaker(bind=e)
session = Session()

query = session.query(Post).filter(and_(Post.use_on_twitter == False,
                                        func.length(Post.description) < 280)).order_by(Post.posted_at).first()
if(query and query.id):
    options = Options()
    options.headless = args.headless

    driver = webdriver.Firefox(options=options)
    driver.set_window_size(600,800)

    login(driver, args.username, args.password)
    add_picture(driver, (dirpath + "/system/" + query.key + ".jpg"), query.description, query.url_target)
    time.sleep(10)

    if args.simulate == False:
        query.use_on_twitter = True
        session.commit()
        driver.find_elements_by_css_selector('[data-testid=tweetButton]')[0].click()
        time.sleep(5)
        driver.close()

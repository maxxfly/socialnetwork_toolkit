# imports
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from random import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import time
import requests
import datetime
import re
import logging
import shutil
import progressbar
import hashlib
import os
import argparse

from datetime import datetime
from lib.post import Post

dirpath = os.getcwd()

def md5sum(filename):
    file = open(filename, 'rb').read()
    return hashlib.md5(file).hexdigest()

parser = argparse.ArgumentParser(description='Grab images from Instagram to save in database')

parser.add_argument('--username', dest='username', action='store', required=True,
                      help='username for Instagram')

parser.add_argument('--headless', dest='headless', action='store_true',
                      help='use headless=True for Firefox')

parser.add_argument('--url_target', dest='url_target', action='store',
                      help='url to add on Twitter message or on click on Pinterest picture'
                    )

args = parser.parse_args()

# classyxdesign
insta_username = args.username
url_target = args.url_target

options = Options()
options.headless = args.headless

driver = webdriver.Firefox(options=options)

# manage database
e = create_engine('sqlite:///data/file.db')
Session = sessionmaker(bind=e)
session = Session()

user_link = 'https://www.instagram.com/{}/'.format(insta_username)

driver.get(user_link)

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

print(">>> Get list of pictures")
post_links = []

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # get pictures
    post_link_elems = driver.find_elements_by_xpath("//a[contains(@href, '/p/')]")

    for post_link_elem in post_link_elems:
        post_link = post_link_elem.get_attribute('href')
        post_links.append(post_link)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

post_links = list(set(post_links))

print(">>> Retrieve each picture")
for post_link in progressbar.progressbar(post_links):
    postid = post_link.split("/")[4]

    query = session.query(Post).filter(Post.key == postid, Post.from_network == "Instagram").count()

    if query > 0: continue

    driver.get(post_link)

    time_element = driver.find_element_by_xpath("//div/a/time")
    post_datetime_str = time_element.get_attribute("datetime")
    post_datetime = datetime.strptime(
        post_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    description_blocks = driver.find_elements_by_css_selector("h2+span")
    description = ""

    if len(description_blocks) > 0:
      description = description_blocks[0].text

    image = driver.find_elements_by_css_selector("img[decoding=auto]")

    if len(image) == 0: continue

    srcs = image[0].get_attribute("srcset")

    target = ""

    for src in srcs.split(','):
        if src.split(" ")[1] == '1080w':
            target = src.split(" ")[0]

    r = requests.get(target, stream=True)

    path = dirpath + "/system/" + str(postid) + ".jpg"

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    md5 = md5sum(path)

    # transform description
    description = re.sub(r"#insta(^\s)*", "", description)
    description = re.sub(r"\s@", " ", description)
    description = re.sub(r"^@", " ", description)

    # save in DB
    post = Post(description=description,
                key=postid,
                url=post_link,
                from_network="Instagram",
                use_on_twitter=False,
                use_on_pinterest=False,
                md5=md5,
                url_target=url_target,
                posted_at=post_datetime)

    session.add(post)
    session.commit()

driver.close()

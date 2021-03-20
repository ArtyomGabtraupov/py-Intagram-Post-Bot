import instagrapi
from instagrapi import Client
import praw
import re
import requests
import os
import random
import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import random
from keep_alive import keep_alive
from PIL import Image

username = '--YOUR USERNAME--'
password = '--YOUR PASSWORD--'

subreddit = "{None}"
title = "{None}"

def uploadPost():
    global subreddit
    global title
    global success

    subreddits = ['dankmemes', 'memes', 'EarthPorn', '2meirl4meirl', 'blursedimages', 'wholesomememes', 'Minecraft', 'forbiddensnacks', 'puns', 'teenagers', 'Intelectuaals', 'BeAmazed', 'Art', 'fakehistoryporn', 'blessedimages', 'technicallythetruth', 'boomershumor', 'bonehurtingjuice', 'AdviceAnimals', 'comedyheaven', 'madlads', 'KamikazeByWords', 'LifeProTips', 'mildlyinteresting', 'mildlyinfuriating', 'clevercomebacks', 'notinteresting']
    for post in reddit.subreddit(subreddits[random.randrange(0, len(subreddits))]).hot(limit=100):
        chance = random.randrange(0, 15)
        #chance = 3
        if chance == 3:
            print("Luck!")
            title = post.title
            author = post.author
            subreddit = post.subreddit
            url = post.url
            file_name = url.split("/")
            if len(file_name) == 0:
                file_name = re.findall("/(.*?)", url)
            file_name = file_name[-1]
            if "." not in file_name:
                file_name += ".jpg"
            if ".jpg" not in file_name or file_name == ".jpg":
                break

            file_name = "img0.jpg"
            r = requests.get(url)
            with open(file_name, "wb") as f:
                f.write(r.content)
            try:
                img = Image.open(file_name)  # open the image file
                img.verify()  # verify that it is, in fact an image
            except (IOError, SyntaxError) as e:
                print('Bad file:', file_name)
                break

            saved_imgs = 10
            for i in range(saved_imgs-1):
                if open("img0.jpg", "rb").read() == open("img"+str(i+1)+".jpg","rb").read():
                    print("Image Already Has Been Posted")
                    break

            img = Image.open(file_name)
            img.close()
            w, h = img.size
            ratio = float(w)/float(h)
            if ratio > 16/9 or ratio < 3/4:
                print("Unacceptable Ratio\n----------------")
                break
            print(f"Proceeding to Upload a Post; r/{subreddit}, {title}\n----------------")
            cl.photo_upload(file_name, caption=f"{title}\n\nCredit: u/{author}, on r/{subreddit}",)
            success = True
            for i in range(saved_imgs-1):
                image = Image.open("img"+str(saved_imgs-2-i)+".jpg")
                image.save("img"+str(saved_imgs-1-i)+".jpg")
            print("Successfully Uploaded Picture\n----------------")
            break
        else:
            print("no luck")

def schedulePost():
    global success
    global reddit
    global cl
    success = False
    print("Logging In")
    cl = Client()
    cl.login(username, password)
    reddit = praw.Reddit(client_id='--YOUR CLIENT ID--', client_secret='--YOUR CLIENT SECRET--', user_agent='my user agent')
    print("Logged In")
    while not success:
        try:
            uploadPost()
        except Exception as ex:
            print(ex)
            print(f"r/{subreddit}\n{title}")
            time.sleep(0.1)

schedule.every().day.at("14:00").do(schedulePost)
schedule.every().day.at("02:00").do(schedulePost)

keep_alive()

while True:
    schedule.run_pending()
    time.sleep(0.5)

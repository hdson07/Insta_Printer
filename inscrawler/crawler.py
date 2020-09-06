from __future__ import unicode_literals

import pyautogui
import random

import glob
import json
import os
import re
import sys
import time
import traceback
from builtins import open
from time import sleep
import psutil

from tqdm import tqdm
from . import secret
from .browser import Browser
from .exceptions import RetryException
from .fetch import fetch_caption
from .fetch import fetch_comments
from .fetch import fetch_datetime
from .fetch import fetch_imgs
from .fetch import fetch_likers
from .fetch import fetch_likes_plays
from .fetch import fetch_details
from .utils import instagram_int
from .utils import randmized_sleep
from .utils import retry
from escpos.connections import getUSBPrinter


from PIL import Image, ImageDraw
from PIL import ImageFilter, ImageFont, ImageOps, ImageChops
import requests
from io import BytesIO

printer_name = "_165_194_35_209"

def mosaic(im,m_size) :
    x_m =im.size[0] % m_size  # 가로 방향 나머지
    y_m =im.size[1] % m_size  # 세로 방향 나머지
    x_new = im.size[0] - x_m  # 가로 방향 새로운 크기
    y_new = im.size[1] - y_m  # 세로 방향 세로운 크기

    im = im.crop((0,0,x_new,y_new))  # crop한 뒤 r로 저장

    x_m =im.size[0] % m_size  # 가로 방향 나머지
    y_m =im.size[1] % m_size  # 세로 방향 나머지
    x_new = im.size[0] - x_m + m_size  # 가로 방향 새로운 크기
    y_new = im.size[1] - y_m + m_size # 세로 방향 세로운 크기



    g_sum = 0
    b_sum = 0
    for i in range(0, im.size[0],m_size):
        for j in range(0, im.size[1],m_size):
            r_sum = 0
            g_sum = 0
            b_sum = 0
            for ii in range(i, i+m_size):
                for jj in range(j, j+m_size):
                    rgb = im.getpixel((ii,jj))
                    r_sum += rgb[0]
                    g_sum += rgb[1]
                    b_sum += rgb[2]
            r_a = round(r_sum/m_size**2)
            g_a = round(g_sum/m_size**2)
            b_a = round(b_sum/m_size**2)
            for ii in range(i, i+m_size):
                for jj in range(j, j+m_size):
                    im.putpixel((ii,jj),(r_a,g_a,b_a))
    return im

def generateImage(item,sleep_list):
    try : 
        username = item['profil_name']
        filename = "./img/" + username + ".png"
        img_url = requests.get(item['img_urls'][0])
        profil_url = requests.get(item['profil_img'])
    except : 
        username = "pickledpiper"
        filename = "./img/" + username + ".png"
        img_url = "no_wifi.png"
        profil_url = "no_wifi.png"

    try : 
        temp_img = Image.open(BytesIO(img_url.content))
    except : 
        temp_img = Image.open('no_wifi.png')
        profil_image = Image.open('no_wifi.png')

    try : 
        profil_image = Image.open(BytesIO(profil_url.content))
    except : 
        profil_image = Image.open('no_wifi.png')

    
    main_mask = Image.open('sample_mask.png')
    main_mask.save(filename)
    time.sleep(sleep_list[0])

    mask_height = main_mask.size[1] + 2
    mask_width = main_mask.size[0] + 2

    font_regular = ImageFont.truetype(r'./fonts/Roboto-Regular.ttf', 16)
    font_bold = ImageFont.truetype(r'./fonts/Roboto-bold.ttf', 16)
    wpercent = (mask_width/float(temp_img.size[0]))
    hsize = int((float(temp_img.size[1])*float(wpercent)))

    pyautogui.click(40, 850)

    #generate profil_maks
    profil_size = (30,30)
    profil_mask = Image.new('L',profil_size,0)

    profil_Draw = ImageDraw.Draw(profil_mask)
    profil_Draw.ellipse((0, 0) + profil_size, fill=255)

   
    profil_image = profil_image.resize(profil_size, Image.ANTIALIAS)

    

    profil_result = ImageOps.fit(profil_image,profil_mask.size,centering=(0.5,0.5))
    profil_result.putalpha(profil_mask)
    # profil_result.show("test")

    profil_result.load()
    main_mask.paste(profil_result,(10,75))

    # main_mask.show("test")
    main_mask.save(filename)


    likes = "Likes " + str(item['likes']) + "s"

    subtitle = item['caption']
    try : 
        subtitle = subtitle.split(" ",1)[1]
        subtitle = subtitle.replace("\n", " ")
        subtitle = subtitle[0:20]

    except :
        pass


    Draw = ImageDraw.Draw(main_mask)
    username_size = Draw.textsize(username)

    modified_username = ''

    for c in username : 
        if random.randint(0,1) == 0 :
            modified_username = modified_username+ '*'
        else : 
            modified_username = modified_username + c
    

    Draw.text((50, 80), modified_username, fill ="black", font = font_bold, align ="left")  
    Draw.text((60+username_size[0]*1.5,80)," Follow",fill =(78,179,220), font = font_bold, align ="left")  
    Draw.text((15, 561), likes, fill ="black", font = font_bold, align ="left")  
    Draw.text((15, 581), modified_username, fill ="black", font = font_bold, align ="left")  
    Draw.text((25+username_size[0]*1.5,581), subtitle, fill ="black", font = font_regular, align ="left")  
    Draw.text((15,601), "more...", fill ="gray", font = font_regular, align ="left")  

    main_mask.save(filename)
    time.sleep(sleep_list[1])

  
    target_img = temp_img.resize((mask_width,hsize), Image.ANTIALIAS)
    # target_img.save('test.jpg') 

    if hsize > mask_width :
        target_img.crop((0,int(hsize/2 - mask_width/2),mask_width,hsize*wpercent))

    white_maks = Image.new("RGB",(mask_width,mask_width),(255,255,255))
    white_maks.paste(target_img,(0,int(mask_width/2 - hsize/2)))

    white_maks = mosaic(white_maks,7)

    # white_maks.show("ase")
    main_mask.paste(white_maks,(0,117))
    main_mask.save(filename)
    time.sleep(sleep_list[2])

 
    os.system("lpr -o media=Upper,letter,Custom.74x119mm -o orientation-requested=6  %s" %(filename))    
    

class Logging(object):
    PREFIX = "instagram-crawler"

    def __init__(self):
        global printer
        try:
            timestamp = int(time.time())
            self.cleanup(timestamp)
            self.logger = open("/tmp/%s-%s.log" % (Logging.PREFIX, timestamp), "w")
            self.log_disable = False

        except Exception:
            self.log_disable = True
        



    def cleanup(self, timestamp):
        days = 86400 * 7
        days_ago_log = "/tmp/%s-%s.log" % (Logging.PREFIX, timestamp - days)
        for log in glob.glob("/tmp/instagram-crawler-*.log"):
            if log < days_ago_log:
                os.remove(log)

    def log(self, msg):
        if self.log_disable:
            return

        self.logger.write(msg + "\n")
        self.logger.flush()

    def __del__(self):
        if self.log_disable:
            return
        self.logger.close()


class InsCrawler(Logging):
    URL = "https://www.instagram.com"
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0
        self.login()

    def _dismiss_login_prompt(self):
        ele_login = self.browser.find_one(".Ls00D .Szr5J")
        if ele_login:
            ele_login.click()

    def login(self):
        browser = self.browser
        url = "%s/accounts/login/" % (InsCrawler.URL)
        browser.get(url)
        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(secret.username)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(secret.password)

        login_btn = browser.find_one(".L3NKy")
        login_btn.click()

        @retry()
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise RetryException()

        check_login()




    def get_latest_posts_by_tag(self, tag, num,sleep_list):
        url = "%s/explore/tags/%s/" % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_posts_full(num,sleep_list)

    def _get_posts_full(self, num,sleep_list):
        dict_posts = {}

        @retry()
        def check_next_post(cur_key):
            ele_a_datetime = browser.find_one(".eo2As .c-Yi7")
            # It takes time to load the post for some users with slow network
            if ele_a_datetime is None:
                raise RetryException()

            next_key = ele_a_datetime.get_attribute("href")
            if cur_key == next_key:
                raise RetryException()

        browser = self.browser
        browser.implicitly_wait(1)
        browser.scroll_down()
        ele_post = browser.find_one(".v1Nh3 a")
        ele_post.click()

        pbar = tqdm(total=num)
        pbar.set_description("fetching")
        cur_key = None

        all_posts = self._get_posts(num)
        i = 1

        # Fetching all posts
        for _ in range(num):
            dict_post = {}


            # Fetching post detail
            try:
                if(i < num):
                    check_next_post(all_posts[i]['key'])
                    i = i + 1

                # Fetching datetime and url as key
                ele_a_datetime = browser.find_one(".eo2As .c-Yi7")
                try:
                    cur_key = ele_a_datetime.get_attribute("href")
                except expression as identifier:
                    sleep(1)
                    cur_key = ele_a_datetime.get_attribute("href")
                    pass                
                dict_post["key"] = cur_key
                fetch_imgs(browser, dict_post)
                fetch_likers(browser, dict_post)
                fetch_likes_plays(browser, dict_post)
                fetch_caption(browser, dict_post)
                profil_img = browser.find_one(".Jv7Aj.pZp3x > * > a img")
                dict_post["profil_img"] = profil_img.get_attribute("src")
                profil_name = browser.find_one(".e1e1d  > * > a")
                if profil_name is not None:
                    dict_post["profil_name"] = profil_name.text
                else :
                    dict_post["profil_name"] = "pickledpiper"
                generateImage(dict_post,sleep_list)
                ele_post = browser.find_one("._65Bje")
                ele_post.click()

            except RetryException:
                sys.stderr.write(
                    "\x1b[1;31m"
                    + "Failed to fetch the post: "
                    + cur_key or 'URL not fetched'
                    + "\x1b[0m"
                    + "\n"
                )
                break

            except Exception:
                sys.stderr.write(
                    "\x1b[1;31m"
                    + "Failed to fetch the post: "
                    + cur_key if isinstance(cur_key,str) else 'URL not fetched'
                    + "\x1b[0m"
                    + "\n"
                )
                traceback.print_exc()

            self.log(json.dumps(dict_post, ensure_ascii=False))
            dict_posts[browser.current_url] = dict_post

            pbar.update(1)

        pbar.close()
        posts = list(dict_posts.values())
        if posts:
            try:
                posts.sort(key=lambda post: post["datetime"], reverse=True)
            except :
                pass 
        
        return posts

    def _get_posts(self, num):
        """
            To get posts, we have to click on the load more
            button and make the browser call post api.
        """
        TIMEOUT = 600
        browser = self.browser
        key_set = set()
        posts = []
        pre_post_num = 0
        wait_time = 1

        pbar = tqdm(total=num)

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find(".v1Nh3 a")
            for ele in ele_posts:
                key = ele.get_attribute("href")
                if key not in key_set:
                    dict_post = { "key": key }
                    # ele_img = browser.find_one(".KL4Bh img", ele)
                    # dict_post["caption"] = ele_img.get_attribute("alt")
                    # dict_post["img_url"] = ele_img.get_attribute("src")

                    # fetch_details(browser, dict_post)
                    # etch_likes_plays(browser, dict_post)

                    key_set.add(key)
                    posts.append(dict_post)

                    if len(posts) == num:
                        break

            if pre_post_num == len(posts):
                pbar.set_description("Wait for %s sec" % (wait_time))
                sleep(wait_time)
                pbar.set_description("fetching")

                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(posts)
            browser.scroll_down()

            return pre_post_num, wait_time

        pbar.set_description("fetching")
        while len(posts) < num and wait_time < TIMEOUT:
            post_num, wait_time = start_fetching(pre_post_num, wait_time)
            pbar.update(post_num - pre_post_num)
            pre_post_num = post_num

            loading = browser.find_one(".W1Bne")
            if not loading and wait_time > TIMEOUT / 2:
                break

        pbar.close()
        print("Done. Fetched %s posts." % (min(len(posts), num)))
        return posts[:num]

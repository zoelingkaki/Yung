# -*- coding:utf-8 -*-

import requests
from lxml import html
import time
from PIL import Image
import json

# 构造headers,大多数网站会检测User-Agent和Referer进行简单的反爬虫
headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/59.0.3071.115 Safari/537.36',
    'Referer': 'www.zhihu.com'
}

# 保持会话
session = requests.Session()


def get_xsrf():
    url = 'https://www.zhihu.com'
    res = session.get(url, headers=headers).content
    sel = html.fromstring(res)
    xsrf = sel.xpath('//input[@name="_xsrf"]/@value')[0]
    return xsrf


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
        image = Image.open('captcha.jpg')
        image.show()
        image.close()
    captcha = input("please input the captcha\n>")
    return captcha


def login():
    loginurl = 'https://www.zhihu.com/login/email'
    formdata = {
        'email': '替换为账号',
        'password': '替换为',
        # 'captcha_type': 'cn',
        '_xsrf': get_xsrf(),
        'captcha': get_captcha()
    }
    loginpage = session.post(loginurl, data=formdata, headers=headers)
    loginpage.encoding = 'utf-8'
    print((json.loads(loginpage.text))['msg'])

if __name__ == '__main__':
    login()

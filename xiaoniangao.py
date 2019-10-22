import os
import time

from selenium import webdriver
from lxml import etree
import requests

browse = webdriver.Chrome()

browse.get('https://www.xiaoniangao.cn/')
time.sleep(1)

html = browse.page_source

html_obj = etree.HTML(html)
img_list = html_obj.xpath('//img/@src')
video_list = html_obj.xpath('//video/@src')

if not os.path.exists('xiaoniangao'):
    os.mkdir('xiaoniangao')

if not os.path.exists('xiaoniangao/img'):
    os.mkdir('xiaoniangao/img')

if not os.path.exists('xiaoniangao/video'):
    os.mkdir('xiaoniangao/video')

for index in range(len(img_list)):
    response = requests.get(img_list[index])
    file_name = str(index) + '.png'
    with open('./xiaoniangao/img/'+file_name,'wb') as f:
        f.write(response.content)
    print('img-----OK')

for index in range(len(video_list)):
    response = requests.get(video_list[index])
    file_name = str(index) + '.mp4'
    with open('./xiaoniangao/video/'+file_name,'wb') as f:
        f.write(response.content)
    print('video-----OK')


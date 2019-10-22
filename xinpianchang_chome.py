import os
import time

from selenium import webdriver
from lxml import etree
import requests

browse = webdriver.Chrome()

browse.get('https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/page-1')
time.sleep(1)

html = browse.page_source

html_obj = etree.HTML(html)
video_list = html_obj.xpath('//li[@class="enter-filmplay"]/@data-articleid')

if not os.path.exists('xinpianchang'):
    os.mkdir('xinpianchang')

for url in video_list:
    browse.get('https://www.xinpianchang.com/a'+url)
    time.sleep(1)
    print("解析视频中...")
    html2 = browse.page_source
    html_obj2 = etree.HTML(html2)
    video_url = html_obj2.xpath('//video/@src')[0]
    print(video_url)

    response =requests.get(video_url)
    with open('xinpianchang/'+url+'.mp4','wb') as f:
        f.write(response.content)
    print('OK')


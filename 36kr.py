import json
import re
import time

import requests
from fake_useragent import UserAgent

headers = {
    'User-Agent': str(UserAgent().random),
}

num = input("请输入获取最新新闻的个数：")

# 一级页面返回json数据
first_response = requests.get('https://36kr.com/pp/api/aggregation-entity?type=web_latest_article&per_page='+num,headers=headers)
first_html = first_response.content.decode('utf-8')
dict_ = json.loads(first_html)

for i in range(int(num)):
    # 获得二级页面id
    id = dict_.get('data').get('items')[i].get('post').get('id')

    second_response = requests.get('https://36kr.com/p/'+str(id),headers=headers)
    second_html = second_response.content.decode('utf-8')

    # 正则匹配规则
    pattern_title = re.compile(r'<h1 class="article-title margin-bottom-20 common-width">(.*?)</h1>',re.S)
    pattern_img = re.compile(r'<p><img.+?src="(.+?)".+?>')

    title = pattern_title.findall(second_html)[0]
    img_url = pattern_img.findall(second_html)

    with open('36kr.txt','a+',encoding='utf-8') as f:
        f.write(title+'\n')
        for j in range(len(img_url)):
            f.write(img_url[j]+'\n')
        f.write('\n')
    print("第"+str(i+1)+"则新闻-----OK")
    time.sleep(2)



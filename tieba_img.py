import os
import time

import requests
from fake_useragent import UserAgent
from lxml import etree


headers = {
        'User-Agent': str(UserAgent().random),
    }



first_response = requests.get("http://tieba.baidu.com/f?kw=%E7%BE%8E%E9%A3%9F&ie=utf-8&pn=0",headers=headers)

first_html = first_response.content.decode('utf-8')
# 去掉网页注释部分
first_html = first_html.replace(r'<!--','').replace(r'-->','')

first_xml = etree.HTML(first_html)
title_list = first_xml.xpath('//div[@class="threadlist_lz clearfix"]/div/a[@rel="noreferrer"]/text()')
link_list = first_xml.xpath('//div[@class="threadlist_lz clearfix"]/div/a[@rel="noreferrer"]/@href')

# 创建文件夹
if not os.path.exists( 'tieba'):
      os.makedirs('tieba')

with open('tieba/tieba.txt','a+',encoding='utf-8') as f:
    for index in range(len(title_list)):
        # 标题
        f.write(title_list[index]+'\n')
        pn = 1
        while True:
            # 二级页面
            second_response = requests.get('http://tieba.baidu.com'+link_list[index]+'?pn='+str(pn),headers=headers)
            second_html = second_response.content.decode('utf-8')
            second_xml = etree.HTML(second_html)
            # 最大页数
            max_page = second_xml.xpath('//li[@class="l_reply_num"][1]/span[2]/text()')[0]
            img_dist =second_xml.xpath('//img[@class="BDE_Image"]/@src')


            for num in range(len(img_dist)):
                f.write(img_dist[num]+'\n')
                # 三级页面
                third_response = requests.get(img_dist[num],headers=headers)
                img = third_response.content

                # 建文件夹
                if not os.path.exists('tieba/'+link_list[index].replace('/','')):
                    os.makedirs('tieba/'+link_list[index].replace('/',''))

                with open('tieba/'+link_list[index].replace('/','')+'/'+str(pn)+'_'+str(num) +'.jpg','wb')as file:
                    file.write(img)
                    print('ok')

                time.sleep(1)
            f.write('\n')

            if pn == int(max_page):
                break
            else:
                pn += 1
        print("ojbk")
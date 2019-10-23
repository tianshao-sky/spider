import json
import time

import requests
from fake_useragent import UserAgent
from lxml import etree
import re

headers = {
    'User-Agent': str(UserAgent().random),
}

list_all_info = []
pn = input('请输入要爬的页面数量（1~20）：')

for page in range(int(pn)):
    #一级页面
    first_response = requests.get('https://hr.163.com/position/list.do?postType=01&currentPage='+str(page+1),headers=headers)
    first_html = first_response.content.decode('utf-8')
    first_xml = etree.HTML(first_html)

    # 职位名称	所属部门	职位类别	工作类型	工作地点	招聘人数	发布时间    二级页面url
    Job_name = first_xml.xpath('//tr/td[1]/a/text()')
    department = first_xml.xpath('//tr/td[2]')
    class_ = first_xml.xpath('//tr/td[3]/text()')
    type_ = first_xml.xpath('//tr/td[4]/text()')
    Work_location =first_xml.xpath('//tr/td[5]/text()')
    num = first_xml.xpath('//tr/td[6]/text()')
    time_ = first_xml.xpath('//tr/td[7]/text()')

    second_url = first_xml.xpath('//tr/td[1]/a/@href')

    for n in department:
        if n.text == None:
            n.text = 'None'


    for i in range(len(Job_name)):
        num_ = re.sub('[\s]','',num[i])
        dict_info = {'职位名称':Job_name[i],'所属部门':department[i].text,'职位类别':class_[i],'工作类型':
                    type_[i],'工作地点':Work_location[i],'招聘人数':num_,'发布时间':time_[i]}

        # 二级页面
        second_response = requests.get('https://hr.163.com'+second_url[i],headers=headers)
        second_html = second_response.content.decode('utf-8')

        second_xml = etree.HTML(second_html)

        # 岗位描述  岗位要求
        description = ''.join(second_xml.xpath('//div[@class="detail-info"]/div[1]/div//text()')).replace('\t','')
        requirements = ''.join(second_xml.xpath('//div[@class="detail-info"]/div[2]/div//text()')).replace('\t','')

        dict_info['岗位描述'] = description
        dict_info['岗位要求'] = requirements

        list_all_info.append(dict_info)

        print('第'+str(page+1)+'页,第'+str(i+1)+'条数据-----OK')

    time.sleep(2)
    print('第'+str(page+1)+'页-----OK')

json_ = json.dumps(list_all_info,ensure_ascii=False,indent=1)
with open('hr163.json','a+',encoding='utf-8') as f:
    f.write(json_)



    
    

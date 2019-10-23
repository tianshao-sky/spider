import json

from jsonpath import jsonpath
import time

import requests
from fake_useragent import UserAgent

def get_cookies():
    headers = {
        'User-Agent': str(UserAgent().random)
    }

    response = requests.get('https://www.lagou.com/jobs/list_python/p-city_6',headers=headers)
    return response.cookies


proxy = {"http": "http://121.232.194.196:9000"}

headers = {
    'User-Agent': str(UserAgent().random),
    'Referer': 'https://www.lagou.com/jobs/list_Python/p-city_6',
}

kd = input('岗位名：')
city = input('城市名：')
start_pn = input('起始页码：')
end_pn = input('结束页码：')

all_info = []
for pn in range(int(start_pn),int(end_pn)+1):
    # query_data = {'needAddtionalResult':'false'}

    data ={
        'first': 'true',
        'pn': pn,
        'kd': kd,
        'sid': '90688bed69e54750becf9c99e0c5a90b'
    }


    first_response = requests.post('https://www.lagou.com/jobs/positionAjax.json?city='+city,data=data,headers=headers,cookies=get_cookies(),proxies=proxy)
    # first_response =first_response.content.decode('utf-8')
    # json_str = json.loads(first_html)
    first_json_ = first_response.json()

    result = jsonpath(first_json_,'$..result')

    for result_ in result[0]:
        items = {}

        # 职位名称
        items['positionName'] = jsonpath(result_,"$..positionName")[0]
        # 薪水
        items['salary'] = jsonpath(result_,"$..salary")[0]
        # 城市
        items['city'] = jsonpath(result_,"$..city")[0]
        # 地区
        items['district'] = jsonpath(result_,"$..district")[0]
        # 创建时间
        items['createTime'] = jsonpath(result_,"$..createTime")[0]
        # 公司规模大小
        items['companySize'] = jsonpath(result_,"$..companySize")[0]
        # 公司全称
        items['companyShortName'] = jsonpath(result_,'$..companyShortName')[0]
        # 公司编号
        items['companyId'] = jsonpath(result_,'$..companyId')[0]

        all_info.append(items)
    print("第"+str(pn)+"页-----OK")

json_ = json.dumps(all_info,ensure_ascii=False,indent=1)
with open('lagou.json','w',encoding='utf-8') as f:
    f.write(json_)




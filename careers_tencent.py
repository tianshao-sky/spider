import json
import time

import requests
from fake_useragent import UserAgent
from multiprocessing import Queue, Process

from pymongo import MongoClient


class Careers_tencent():
    def __init__(self):
        self.headers = {
            'User-Agent': str(UserAgent().random)
        }
        self.proxies = {
            "http": "http://39.108.90.252:8000"
        }
        self.pn = 1
        self.params = {
                'timestamp': str(int(time.time() * 1000)),
                'countryId': '',
                'cityId': '',
                'bgIds': '',
                'productId': '',
                'categoryId': '40001001,40001002,40001003,40001004,40001005,40001006',
                'parentCategoryId': '',
                'attrId': '',
                'keyword': '',
                'pageIndex': self.pn,
                'pageSize': 10,
                'language': 'zh-cn',
                'area': 'cn',
            }
        self.careers = []


    def sent_request(self):
        response = requests.get('https://careers.tencent.com/tencentcareer/api/post/Query',params=self.params,headers=self.headers,proxies=self.proxies)
        html = response.content.decode()
        return_json = json.loads(html)
        return return_json


    def analyze(self,return_json):
            careers_list = return_json.get('Data').get('Posts')

            for career in careers_list:
                items = {}
                # 职位名
                items['RecruitPostName'] = career.get('RecruitPostName')
                # 拱墅名
                BGName = career.get('BGName')
                # 城市
                LocationName = career.get('LocationName')
                # 国家
                CountryName = career.get('CountryName')
                # 种类
                CategoryName = career.get('CategoryName')
                # 时间
                LastUpdateTime = career.get('LastUpdateTime')
                items['PostURL'] = career.get('PostURL')

                items['info'] = BGName + '|' + LocationName + ',' + CountryName + '|' + CategoryName + '|' + LastUpdateTime

                self.careers.append(items)

    def save(self):
        client = MongoClient(host="127.0.0.1", port=27017, )
        db = client.careers
        db.carrer.insert_many(self.careers)

    def main(self):
        page = input('页数:')
        for pn in range(1,int(page)+1):
            self.pn = pn
            return_json = self.sent_request()
            self.analyze(return_json)
            print(str(pn)+'-----OK')
        self.save()


if __name__ == '__main__':
    careers_tencent = Careers_tencent()
    careers_tencent.main()

import json

import requests
from fake_useragent import UserAgent
from lxml import etree

from pymongo import MongoClient

class Ctrip():
    def __init__(self):
        self.headers =  {
            'User-Agent': str(UserAgent().random)
        }
        self.proxies = {
            "http": "http://39.108.90.252:8000"
        }
        self.all_info = []


    def send_request(self,data):
        response = requests.post('https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx', data=data,headers=self.headers, proxies=self.proxies)
        html = response.content.decode('utf-8').replace('\\"', '"')
        return html
    
    def send_request2(self,id,pn):
        data = {"hotelId": id,
                     "pageIndex": pn,
                     "tagId": 0,
                     "pageSize": 10,
                     "groupTypeBitMap": 3,
                     "needStatisticInfo": 1,
                     "order": 1,
                     # "basicRoomName":"",
                     "travelType": -1,
                     # "head":{
                     #     "cid":"09031015111398998348",
                     #     "ctok":"",
                     #     "cver":"1.0",
                     #     "lang":"01",
                     #     "sid":"8888",
                     #     "syscode":"09",
                     #     "auth":"",
                     #     "extension":[]
                     # }
                     }
        response = requests.post('http://m.ctrip.com/restapi/soa2/16765/gethotelcomment', json=data,headers=self.headers)
        html = response.content.decode('utf-8')
        return html

    def analyze(self,html):
        first_xml = etree.HTML(html)
        nodes = first_xml.xpath('//div[@class="hotel_new_list J_HotelListBaseCell"]')

        for node in nodes:
            info = {}
            # 酒店名
            info['name'] = node.xpath('./ul/li[@class="hotel_item_name"]/h2/a/text()')[0].strip()
            # 酒店类型
            info['hotel_type'] = node.xpath('./ul/li[@class="hotel_item_name"]/span/span[last()]/@title')[0].strip()
            # 区名
            area = node.xpath('./ul/li[@class="hotel_item_name"]/p/a[1]/text()')[0].strip()
            # 地点
            location = node.xpath('./ul/li[@class="hotel_item_name"]/p[1]/text()')[-1][1:-1].strip()
            # 评论人数(0是好评率,1是评论人数)
            comment = node.xpath('./ul/li[@class="hotel_item_judge no_comment "]/div/a/span/span/text()')
            if comment == []:
                info['people_num'] = '暂无人点评'
            else:
                info['people_num'] = comment[1]
            # 最低价
            info['low_price'] = node.xpath('./@data-maidian')[0].split(",")[4]
            # 二级页面url
            id = node.xpath('./@id')[0]
            # 地址
            info['address'] = '[' + area + '] ' + location

            pn = 0
            comment_info_list = []
            while True:
                pn += 1
                html = self.send_request2(id,pn)

                json_ = json.loads(html)
                if pn == 1:
                    # 卫生
                    info['healthPoint'] = json_.get('statisticInfo').get('healthPoint')
                    # 环境
                    info['environmentPoint'] = json_.get('statisticInfo').get('environmentPoint')
                    # 服务
                    info['servicePoint'] = json_.get('statisticInfo').get('servicePoint')
                    # 设施
                    info['facilityPoint'] = json_.get('statisticInfo').get('facilityPoint')

                if pn == 3 or json_.get('othersCommentList')==[]:
                    info['comment_info_list'] = comment_info_list
                    break

                for node in json_.get('othersCommentList'):
                    comment_info = {}
                    # 用户id
                    comment_info['id'] = node.get('id')
                    # 用户名
                    comment_info['userNickName'] = node.get('userNickName')
                    # 房型
                    comment_info['baseRoomName'] = node.get('baseRoomName')
                    # 出游类型
                    comment_info['travelType'] = node.get('travelType')
                    # 入住时间
                    comment_info['checkInDate'] = node.get('checkInDate')
                    # 评价
                    comment_info['content'] = node.get('content')
                    # 有用数
                    comment_info['usefulNumber'] = node.get('usefulNumber')

                    comment_info_list.append(comment_info)
            self.all_info.append(info)
            print('一个酒店-----OK')

    def save(self):
        # print(self.all_info)
        client = MongoClient(host="127.0.0.1", port=27017, )
        db = client.ctrip
        db.ctrip.insert_many(self.all_info)

    def main(self):
        start_page = input('起始页:')
        end_page = input('结束页:')
        for page in range(int(start_page),int(end_page)+1):
            data = {
                'page': page,
                'cityId': '1',
            }
            html = self.send_request(data)
            self.analyze(html)
        self.save()

if __name__ == '__main__':
    ctrip = Ctrip()
    ctrip.main()


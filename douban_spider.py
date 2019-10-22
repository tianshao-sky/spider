#coding:utf-8

import json
import random
import time
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider():
    def __init__(self):

        self.star_rank = int(raw_input("请输入起始排名："))
        self.end_rank = int(raw_input("请输入结束排名："))
        ua_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"
        ]

        user_agent = random.choice(ua_list)

        self.headers = {
            'User-Agent': user_agent

        }

    def send_request(self,url):
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        return response


    def save(self,response):
        html = response.read()
        dict_unicode = json.loads(html)[0]


        with open('douban_top.txt','a+') as f:
            # 片名
            f.write('片名:'+dict_unicode['title']+'\n')
            # 时间
            f.write('时间:'+dict_unicode["release_date"]+'\n')
            # 国家
            f.write('国家:'+dict_unicode["regions"][0]+'\n')
            # 演员
            f.write('演员:')
            for j in dict_unicode["actors"]:
                f.write(j+'/')
            # 评分
            f.write('\n'+'评分:'+dict_unicode["score"]+'\n')
            # 图片
            f.write('图片:'+dict_unicode['cover_url']+'\n'+'\n')


    def main(self):
        for i in range(self.star_rank-1, self.end_rank - self.star_rank + 1):
            url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start='+str(i)+'&limit=1'
            response = self.send_request(url)

            self.save(response)
            print('top'+str(i+1)+' is ok')
            time.sleep(2)


if __name__ == '__main__':
    spider=Spider()
    spider.main()

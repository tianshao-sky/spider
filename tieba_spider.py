#coding:utf-8
import random
import time
import urllib2
import urllib

class Spider():
    def __init__(self):
        self.name = raw_input("请输入贴吧名：")
        self.star_page = int(raw_input("请输入起始页："))
        self.end_page = int(raw_input("请输入结束页："))
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

    def save(self,response,i):
        html = response.read()
        with open(self.name + '吧_' + str(i) + '.html', 'w') as f:
            f.write(html)


    def main(self):
        for i in range(self.star_page, self.end_page + 1):
            page_num = str(50 * (i - 1))
            url = 'https://tieba.baidu.com/f?ie=utf-8&%s&fr=search&pn=%s' % (urllib.urlencode({'kw': self.name}), page_num)
            response = self.send_request(url)
            self.save(response,i)
            print('第' + str(i) + '页————OK')
            time.sleep(2)


if __name__ == '__main__':
    spider=Spider()
    spider.main()

import json
import random
import time
import urllib

from urllib import request,parse

ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"
]

user_agent = random.choice(ua_list)

headers = {
    'User-Agent': user_agent,
    "Referer": "https://fanyi.qq.com/",


}

time_chuo = str(int(time.time()*1000))

text =input('请输入要翻译的：')

data = {
    'source': 'auto',
    'target': 'zh',
    'sourceText': text,
    'qtv': '42214eac9556400e',
    'qtk': 't8NSuO7k+yPSporbXZqXo/bJNfMRmCV8bF+Ui4DltjKisGvYFCqs0lujxxUBv6boXBkZAYhyPkDnAYOyLTtOQTqTCtNPHu49xkVg00FphJL++yQ1DeH+cqlSl3SlrPkYr1aykmlNQfV4csVV1z1juA==',
    'sessionUuid': 'translate_uuid'+ time_chuo
}

form_data = urllib.parse.urlencode(data).encode('utf-8')
headers['Content-Length'] = len(form_data)

request1 = urllib.request.Request('https://fanyi.qq.com/api/translate',data=form_data,headers=headers)

response =urllib.request.urlopen(request1)

json_data = json.loads(response.read().decode())

result = json_data['translate']['records'][0]['targetText']

print('翻译结果：'+result)
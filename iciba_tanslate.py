import json
import random
import time
import urllib
from fake_useragent import UserAgent

from urllib import request,parse

# ua_list = [
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
#     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
#     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6"
# ]
#
# user_agent = random.choice(ua_list)

headers = {
    'User-Agent': str(UserAgent().random),

}


text =input('请输入要翻译的：')

data = {
'f': 'auto',
't': 'auto',
'w': text
}

form_data = urllib.parse.urlencode(data).encode("utf-8")

request1 = urllib.request.Request("http://fy.iciba.com/ajax.php?a=fy",data=form_data,headers=headers)

response =urllib.request.urlopen(request1)

json_data = json.loads(response.read().decode())


result = json_data.get('content').get('out')
if result == None:
    result_list = json_data.get('content').get('word_mean')
    result = ''
    for i in result_list:
        result += i

print('翻译结果为：'+ result)
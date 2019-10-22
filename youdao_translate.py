import hashlib
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
    'Referer':'http://fanyi.youdao.com/',
    "Cookie":" OUTFOX_SEARCH_USER_ID=1449344671@10.108.160.14",
}

time_chuo = time.time()*1000

text =input('请输入要翻译的：')

e = text
i = str(time_chuo) + str(random.randint(0,9))
sign = hashlib.md5(("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj").encode()).hexdigest()

data = {
'i':text,
'from':'AUTO',
'to':'AUTO',
'smartresult':'dict',
'client':'fanyideskweb',
'salt': i,
'sign':sign,
'ts':str(time_chuo),
'bv':'01d5c9278d5fc19a9a9367e8cbca7110',
'doctype':'json',
'version':'2.1',
'keyfrom':'fanyi.web',
'action':'FY_BY_REALTlME',
}

form_data = urllib.parse.urlencode(data).encode("utf-8")
headers['Content-Length'] = len(form_data)

request1 = urllib.request.Request("http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule",data=form_data,headers=headers)

response =urllib.request.urlopen(request1)

json_data = json.loads(response.read().decode())

result = json_data['translateResult'][0][0]['tgt']

print('翻译结果为：'+ result)

import requests
from fake_useragent import UserAgent

ssion = requests.session()

headers = {
    "User-Agent" : str(UserAgent().random)
}

data = {
    'email':'账号',
    'password':'密码'
}

ssion.post("http://www.renren.com/PLogin.do",data=data,headers=headers)

response = ssion.get("http://www.renren.com/928944480/profile")

print(response.text)

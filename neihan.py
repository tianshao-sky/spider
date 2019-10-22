import re
import requests
from fake_useragent import UserAgent

from lxml import etree

page = 0

while True:
    page += 1

    headers = {
        'User-Agent': str(UserAgent().random),

    }

    response = requests.get("https://www.neihan-8.com/article/list_5_"+str(page)+".html",headers=headers)

    html=response.content.decode("gbk")

    # pattern1 = re.compile(r'<h4>[\s]+<a href="/article/[0-9]{5}.html">(.*?)</h4>',re.S)
    # pattern2 = re.compile(r'<div class="f18 mb20">[\s]+(.*?)</div>',re.S)
    #
    # titles = pattern1.findall(html)
    # duanzis = pattern2.findall(html)
    #
    # with open('neihan.txt','a+',encoding='utf-8') as f:
    #
    #     for j in range(len(titles)):
    #         title = titles[j].replace('</a><span class="new">new</span>','').replace('</b></a>','').replace('<b>','').replace('</a>','')
    #         f.write(title+'\n')
    #         result = re.sub('[\s]+',"",duanzis[j])
    #         result = result.replace('</p>\r\n<p>\r\n\t\u3000\u3000','').replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&hellip;','...').replace('</p>',"").replace("<p>","").replace("<br/>",'\n').replace('&quot;','"')
    #         f.write(result+'\n\n')
    #     print("第"+str(page)+"页----OK")
    #
    # flag = input("按回车继续，q退出！\n")
    #
    # if flag == 'q':
    #     break

    html_obj = etree.HTML(html)
    content_list = html_obj.xpath('//div[@class="f18 mb20"]/text()')
    print(content_list)
    break

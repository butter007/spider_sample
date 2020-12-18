import requests

import os
from lxml import html
proxies = {"http": "http://193.38.51.182:55555"}
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Referer": "https://pos.baidu.com/"
}
res = requests.get("https://www.xiachufang.com",
                   headers=headers,
                   proxies=proxies)
print(res.status_code)

etree = html.etree
htmlcon = etree.HTML(res.text)

li = []
filepath = "D:\\xiachufang"
re = htmlcon.xpath('//ul[@class="plain"]/li/div/a/img')
for item in re:
    li.append(item.get('src').split('?')[0])
if not os.path.exists(filepath):
    os.makedirs(filepath)

for item in li:
    r = requests.get(item)
    with open(os.path.join(filepath, item.split("/")[-1]), "wb") as fp:
        for chunk in r.iter_content(chunk_size=1024):
            fp.write(chunk)

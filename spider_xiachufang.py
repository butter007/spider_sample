import requests

import os
from lxml import html


def get_pic(url, headers, proxies):
    etree = html.etree
    filepath = "D:\\xiachufang"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    for i in range(1, 26):
        res = requests.get(url, headers=headers, proxies=proxies)

        htmlcon = etree.HTML(res.text)

        li = []

        re = htmlcon.xpath("//div[@class='cover pure-u']/img/@data-src")
        for item in re:
            li.append(item.split('?')[0])

        for item in li:
            r = requests.get(item)
            with open(os.path.join(filepath, item.split("/")[-1]), "wb") as fp:
                for chunk in r.iter_content(chunk_size=1024):
                    fp.write(chunk)
        print("第 %s 页" % i)


if __name__ == "__main__":
    url_start = "https://www.xiachufang.com/category/"
    proxies = {"http": "http://193.38.51.182:55555"}
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Referer": "https://pos.baidu.com/"
    }
    numbers = [40076, 40077, 40078, 51848, 52354, 51743, 52351, 51940]
    for number in numbers:
        print(number)
        for page in range(1, 26):
            url = "%s%s/?page=%s" % (url_start, number, page)
            get_pic(url, headers=headers, proxies=proxies)

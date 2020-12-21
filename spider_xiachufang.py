import requests
import os
from lxml import etree


# 请求url获取结果
def fetch(url, headers, proxies):
    res = requests.get(url, headers, proxies)
    if res.status_code != 200:
        res.raise_for_status()
    return res.text


# 根据大类获取每一类的页面加入links
def getpages(str):
    numbers = [40076, 40077, 40078, 51848, 52354, 51743, 52351, 51940]
    pages = []
    for number in numbers:
        print(number)
        for page in range(1, 26):
            url = "%s%s/?page=%s" % (url_start, number, page)
            pages.append(url)
    return pages


def getimglinks(pageurl, headers, proxies):
    li = []
    pagecon = fetch(pageurl, headers, proxies)
    selector = pagecon.xpath("//div[@class='cover pure-u']/img/@data-src")
    for item in selector:
        li.append(item.split('?')[0])
    return li


# 下载页面
def download_pic(imgurl, headers, proxies, filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    r = requests.get(imgurl, headers, proxies)
    with open(os.path.join(filepath, imgurl.split("/")[-1]), "wb") as fp:
        for chunk in r.iter_content(chunk_size=1024):
            fp.write(chunk)


if __name__ == "__main__":
    url_start = "https://www.xiachufang.com/category/"
    proxies = {"http": "http://193.38.51.182:55555"}
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Referer": "https://pos.baidu.com/"
    }
    filepath = "D:\\xiachufang"
    links = []
    for item in getpages(url_start):
        links.extend(getimglinks(item, headers, proxies))
    print(links)

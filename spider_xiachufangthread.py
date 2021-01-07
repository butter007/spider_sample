import requests
import os
from lxml import etree
import time
import threading
from queue import Queue

link_queue = Queue()
threads_num = 10
threads = []
download_pages = 0


# 请求url获取结果
def fetch(url, headers, proxies):
    res = requests.get(url, headers=headers, proxies=proxies)
    if res.status_code != 200:
        print(res.status_code)
        res.raise_for_status()
    global download_pages
    download_pages += 1
    return res.text


# 根据大类获取每一类的页面加入links
def getpages(str):
    numbers = [40078, 40077, 40078, 51848, 52354, 51743, 52351, 51940]
    pages = []
    for number in numbers:
        for page in range(1, 26):
            url = "%s%s/?page=%s" % (url_start, number, page)
            pages.append(url)
    return pages


def getimglinks(pageurl, headers, proxies):
    li = []
    pagecon = fetch(pageurl, headers, proxies)
    re = etree.HTML(pagecon)
    selector = re.xpath("//div[@class='cover pure-u']/img/@data-src")
    for item in selector:
        li.append(item.split('?')[0])
    return li


# 下载页面
def download_pic(imgurl, headers, proxies, filepath):
    r = requests.get(imgurl, headers=headers, proxies=proxies)
    with open(os.path.join(filepath, imgurl.split("/")[-1]), "wb") as fp:
        for chunk in r.iter_content(chunk_size=1024):
            fp.write(chunk)


def download(headers, proxies, filepath):
    while True:
        # 阻塞直到从队列里获取一条消息
        link = link_queue.get()
        if link is None:
            break
        download_pic(link, headers, proxies, filepath)
        link_queue.task_done()
        print("remaining queue: %s" % link_queue.qsize())


if __name__ == "__main__":
    starttime = time.time()
    url_start = "https://www.xiachufang.com/category/"
    proxies = {"http": "http://193.38.51.182:55555"}
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Referer": "https://pos.baidu.com/"
    }
    filepath = "D:\\xiachufang"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    links = []
    for item in getpages(url_start):
        links.extend(getimglinks(item, headers, proxies))
    for imgurl in links:
        link_queue.put(imgurl)
    # download_pic(imgurl, headers, proxies, filepath)
    # 启动线程，并将线程对象放入一个列表保存
    for i in range(threads_num):
        t = threading.Thread(target=download,
                             args=(headers, proxies, filepath))
        t.daemon = True
        t.start()
        threads.append(t)
    # 阻塞队列，知道队列被清空
    link_queue.join()
    # 向队列放入N个None，以通知线程退出
    for i in range(threads_num):
        link_queue.put(None)
    # 退出线程
    for t in threads:
        t.join()
    print("down load finished")
    print("download %s pages" % download_pages)
    print("time last", time.time() - starttime)

import requests
from bs4 import BeautifulSoup
proxies = {"http": "http://193.38.51.182:55555"}
res = requests.get("http://xiachufang.com", proxies=proxies)

soup = BeautifulSoup(res.text, "lxml")
print(soup.prettify())

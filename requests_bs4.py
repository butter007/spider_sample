import requests
from bs4 import BeautifulSoup
proxies = {"http","http://193.38.51.182:55555"}
res = requests.get("http://httpbin.org/ip",proxies=proxies)
print(res.text)
"""

res = requests.get("http://httpbin.org/ip",)
print(res.json())

soup = BeautifulSoup(res.text)
soup.prettyfy()
"""

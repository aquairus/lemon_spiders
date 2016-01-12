import requests
import sys
from bs4 import BeautifulSoup
import re

reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_info(url):
	r = requests.get(url)
	print r.text
	print r.encoding 

start_url="https://zh.wikipedia.org/wiki/Category:按國籍分類"
get_info(start_url)
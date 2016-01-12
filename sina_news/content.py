# -*- coding:utf-8 -*-
import requests
import sys
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )





start_url = "http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml"

current_url=start_url


r = requests.get(current_url)
r.encoding="utf-8" 
text=r.text
soup = BeautifulSoup(text)
#print text
for next in soup.find_all('span',class_="pagebox_next"):
	print next.a.get("href")
#print soup.find_all('span',class_="pagebox_next")[1].a.get('href')
#	print next
# url="http://news.sina.com.cn/c/nd/2015-12-20/doc-ifxneefs5603228.shtml"
# m = re.search('.*/doc-i(.*).shtml', url)
# info="http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-"+m.group(1)+\
# "&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&+jsvar=loader_1452079153841_74035442"
# r = requests.get(info) 
# text=r.text
# m = re.findall(r"content\":(.*?),", r.text)
# review=u''
# #print type(review)
# for content in m:
# 	review+=unicode(str(content))
# print review.decode("unicode-escape")
# 	#print content
	#print unicode(content.encode("utf-8"))
	#print type(unicode(content.encode("utf-8")))

#	print unicode(content, "utf-8")
#	print type(unicode(content, "utf-8"))
	#print type(content)
	#print repr(content) 
	#print content.decode('utf-8')

#print r.encoding
#print r.text
#print r.headers['content-type']
#print r.json()


#for review in soup.find_all('div',class_="info"):
#	print review 
#print content
#front="http://roll.news.sina.com.cn/news/gnxw/gdxw1/"
# #tail=soup.find_all('span',class_="pagebox_next")[0].a.get('href')[2:]

# '''
# ox_next")[0].a.get('href')[2:]
# http://comment5.news.sina.com.cn/page/info?version=1&format=j
# s&channel=gn&newsid=comos-fxmszek7418849&group=&compress=0&ie
# =utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_1452079153841_74035442
# fxmszek7418849.shtml

# "http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-"+fxmszek7418849+
# "&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&+jsvar=loader_1452079153841_74035442

# http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fxneefs5603228&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_3352079632331_36714345

# getGuid = function() {
#         return Math.abs((new Date).getTime()) + "_" + Math.round(1e8 * Math.random())
#     }
# '''

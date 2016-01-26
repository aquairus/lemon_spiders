#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import requests
import sys
#from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )
debug=0
page_num=3

class news():
	def __init__(self, url,title):
		self.type = "news"
		self.url = url 
		self.title = title
		self.content=self.get_content(url)
		self.review =self.get_review(url)
		m = re.search('.*/(\d+)-(\d+)-(\d+)/.*', url)
		self.time =m.group(1)+m.group(2)+m.group(3)

	def get_review(self,url):
		#url="http://news.sina.com.cn/c/nd/2015-12-20/doc-ifxneefs5603228.shtml"
		m = re.search('.*/doc-i(.*).shtml', url)
		info="http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-"+m.group(1)+\
		"&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&+jsvar=loader_1452079153841_74035442"
		r = requests.get(info) 
		text=r.text
		m = re.findall(r"content\":(.*?),", r.text)
		review=u''
		for content in m:
			review+=content+"<p>"
		return review.decode("unicode-escape")
	
	def get_content(self,url):
		r = requests.get(url)  
		r.encoding="gb2313"
		text=r.text
		#print(type(text))
		#text=text.replace("<p>","<p>page").replace("<br>","br") 
		soup = BeautifulSoup(text.replace("<br>","br") )
		content=""
		for line in soup.find_all('p')[1:-3]:
			content+=line.get_text()+"<p>" #+"<br>"
		return content.replace("br","<br>")
		#.replace("br","<br>").replace("page","<p>")
		
	def p(self):
		print(self.title)
		print(self.url)
		print(self.time)
		print(self.content[:20])
		print(self.review)
		print("---")

	def get_dict(self):
		news_dict={
		"review":self.review,
		"url":self.url,
		"time":self.time,
		"title":self.title,
		"content":self.content,
		"type":self.type
		}
		return news_dict


out_file =open('news_ouput.txt','w+')

prefix="http://roll.news.sina.com.cn/news/gnxw/gdxw1"
start_url = "http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml"
current_url=start_url

for page in range(page_num):
	r = requests.get(current_url)
	r.encoding="gbk"
	text=r.text
	soup = BeautifulSoup(text,"lxml")
	current_url=prefix+soup.find_all('span',class_="pagebox_next")[0].a.get('href')[1:]

	for link in soup.find_all('a')[:45]:
		href=link.get('href')
		m = re.search('http://news.sina.com.cn/[c|o]/.*', href)
		if m:
			new_one=news(m.group(0),link.get_text())
			news_dict=new_one.get_dict()
			if debug:
				for k,v in news_dict.items():
					print k+":"+v
			else:	
				out_file.write("{")
				for k,v in news_dict.items()[:-1]:
					out_file.write("\""+k+"\""+":"+"\""+v+"\""",")
				k,v=news_dict.items()[-1]
				out_file.write("\""+k+"\""+":"+"\""+v+"\"")
				out_file.write("}\n")


out_file.close()
print "finish "




		#print (news_dict)
		#print news_dict["title"]
		#print ""
		#print >> out_file,json.dumps(news_dict)
		



		#new_data=json.loads(new_one.get_dict())
		#stack.append (json.dumps(new_one.get_dict())
		#out_file.writelines(json.dumps(news_dict))
		#print json.dumps(new_one.get_dict())
		#print new_one.get_dict()		#new_one.p()




		#print(link.get_text())

		#.encode("utf-8"))#.decode("utf-8"))

#print r.headers
# s = requests.session()
# r = s.post(url, cookies=cookies, data=form)
# d = pq(r.text)


# class news():
# 	def __init__(self, name, points, courseType):
# 		self.type = news
# 		self.url = url 
# 		self.title = title
# 		self.content=""
# 		self.time =""
# 		self.review =""

# {
# 	"type": "news",
# 	"content": "【环球时报综合报道】\"伴随着天津港船舶的鸣笛声，现场搜救人员举行默哀一分钟悼念活动\"，\"德国之声\"18日报道了天津为遇难者举行的悼念仪式：\n事故现场约80名消防官兵，每人手持一支白色菊花，集体脱帽为遇难者默哀。报道称，实际上，从周一晚间开始，就有天津市民陆续以点燃蜡烛的方式举行祭奠活\n动。互联网照片显示，有民众用蜡烛摆出\"8.12，滨海加油\"的字样。 \n\n\n　　据香港\"文汇网\"报道，天津港\"8.12\"特别重大火灾爆炸事故悼念活动于18日上午9时许开始，分别在6个不同地方举行，主会场为天津滨海新区京门大街街心公园。天津市主要领导和社会各界代表300多人参加主会场的悼念活动。",
# 	"title": "天津爆炸仓库所有权成谜 外媒:大老板未浮出",
# 	"time": 20150819,
# 	"url": "http://news.sina.com.cn/c/2015-08-19/072232221525.shtml",
# 	"review": "查财务、钱都给谁了<p>大股东李亮今年34岁，其父母是天津市东丽区老干部局和供热站的普通员工”？？说笑话了吧！他可是出资人啊，普通员工之家能在一家公司里出资400万，在公司里占55%股份，莫不是继承了世界银行的财产不成？<p>为天津爆炸事件祈祷，愿逝者安息，愿幸存者快点给救出来"
# }
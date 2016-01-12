import requests
import sys
#from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )
debug=1
page_num=1

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
		print(type(text))
		#text=text.replace("<p>","<p>page").replace("<br>","br") 
		soup = BeautifulSoup(text.replace("<br>","br") )
		content=""
		for line in soup.find_all('p')[1:-3]:
			content+=line.get_text()+"<p>" 
		return content.replace("br","<br>")
		
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
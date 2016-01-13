#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import requests 
from requests import ConnectionError
import sys
from bs4 import BeautifulSoup
import re
import time
import threadpool
import Queue
from time import sleep
import random
from pybloom import BloomFilter



reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=12
delay =1
pause=40
vocation=100

exp = re.compile(ur'.{5,}')
en_exp = re.compile(ur'.*?·.*')

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }


def write_names(name):
	#print name
	if en_exp.match(name):
		bd_en.write(name+"\n")
	else:
		if not exp.match(name):
			bd_of.write(name+"\n")


def get_content(url):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text


	except BaseException, e:
		urlqueue.put(url)
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	childen=[]
	NodeList=soup.find_all('a',class_="title nslog:7450")
	for child in NodeList:
		write_names(child.text)

	next=soup.find_all(id='next')
	if len(next)>0:
		return	next[0].get("href")
	else:
		return None


def new_node(url):
	childen,flag=get_children(url)

	#print "child"
	#print flag
	if flag>1:
		for child in childen:
			if not child in urlfilter:
				urlqueue.put(child)
				urlfilter.add(child)


	next=get_content(url)

	while next:
		next=get_content(pre_url_fenlei+next)




def get_children(url):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text


	except BaseException, e:
		urlqueue.put(url)
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	childen=[]
	NodeList=soup.find_all('div',class_="category-title")
	length=len(NodeList)
	if length>1:
		for i in range(length-1):
			for child in NodeList[i].find_all("a"):
				print child.text
				childen.append(pre_url+child.get("href"))
		return childen,length
	else:
		return None,0



start_url=[
"http://baike.baidu.com/fenlei/社会科学人物",
"http://baike.baidu.com/fenlei/政治人物",
"http://baike.baidu.com/fenlei/经济人物",
"http://baike.baidu.com/fenlei/虚拟人物",
"http://baike.baidu.com/fenlei/社会人物",
"http://baike.baidu.com/fenlei/文化人物",
"http://baike.baidu.com/fenlei/社会人物",
"http://baike.baidu.com/fenlei/自然科学人物"]

test_url=[
"http://baike.baidu.com/fenlei/社会科学人物"]

pre_url="http://baike.baidu.com"
pre_url_fenlei="http://baike.baidu.com/fenlei/"

bd_of =open('../baidu_name.txt','w+')
bd_en=open('../en.txt','w+')


urlfilter = BloomFilter(capacity=10000, error_rate=0.001)
urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt) 
start_time=time.time()
for url in start_url:
	urlqueue._put(url)
	

while not urlqueue.empty():
	data=[urlqueue.get()]
	works = threadpool.makeRequests(new_node, data)
	[pool.putRequest(work) for work in works]

 	sleep(delay)
 	t=time.time()-start_time
 	if int(t)%pause==0:
 		sleep( random.randint(vocation/2,vocation))

pool.wait()


bd_of.close()
bd_en.close()

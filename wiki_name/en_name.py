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



reload(sys)
sys.setdefaultencoding( "utf-8" )

global cnt
scale=-1
debug=1
thread_cnt=16
delay =0.4
pause=50
vocation=1

pre_url="https://zh.wikipedia.org"

exp = re.compile(ur'.*?·.*')
exp_ch = re.compile(ur'(中國|中国|華|香港|日本|台灣|民國|中東|韓國|埃及|伊斯兰|越南|朝鮮)')
list_exp = re.compile(ur'.*列表')



def get_children(url):
	try:
		r = requests.get(url)
		text=r.text
	except BaseException, e:
		urlqueue.put(url)
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	childen=[]
	for child in soup.find_all('a',class_="CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory"):
		m = exp_ch.search(child.text)
		if not m:
			childen.append(pre_url+child.get("href"))
	return childen

def get_list(url):
	try:
		r = requests.get(url)
		text=r.text
	except ConnectionError, e:
		urlqueue.put(url)
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	names=[]

	for item in soup.find_all('a',class_="new"):
			names.append(item.text)
	return names


def get_names(url):
	try:
		r = requests.get(url)
		text=r.text
	except ConnectionError, e:
		urlqueue.put(url)
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	names=[]
	
	childlist=soup.find_all('a',class_="CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory")
	if not childlist:

		for item in soup.find_all('div',class_="mw-category-group")[:-2]:
			if not list_exp.match(item.ul.li.a.text):
				names.append(item.ul.li.a.text)
			else:
				names=names+get_list(pre_url+item.ul.li.a.get("href"))

	return names





def new_category(url):
	return category(url)


class category():
	def __init__(self, url):
		self.url = url 
		self.child_urls =get_children(url)
		self.names=[]

		if not self.child_urls:
			self.names=get_names(url)
			self.print_names()
			self.write_names(wiki_of)

		else:
			for i in self.child_urls[:scale]:
				urlqueue.put(i)

	def print_names(self):
		global cnt
		cnt+=1
		if cnt%10==0:
			print cnt
		for name in self.names:
			print name

	def write_names(self,of):
		for name in self.names:
			if exp.match(name):
				of.write(name+"\n")



	


pre_url="https://zh.wikipedia.org"
test_url="https://zh.wikipedia.org/wiki/Category:日本的大學教師"
test2_url="https://zh.wikipedia.org/wiki/Category:各國政治人物"
start_url="https://zh.wikipedia.org/wiki/Category:按國籍分類"

wiki_of =open('english.txt','w+')

urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt) 
start_time=time.time()
cnt=0


root=category(start_url)

while not urlqueue.empty():
	data=[urlqueue.get()]
	works = threadpool.makeRequests(new_category, data)
	[pool.putRequest(work) for work in works]
 	sleep(delay)
 	t=time.time()-start_time
 	if int(t)%pause==0:
 		sleep(vocation)
pool.wait()
print time.time()-start_time
print "All subprocesses done."
wiki_of.close()

# def get_info(url):
# 	r = requests.get(url)
# 	print r.text
# 	print r.encoding 

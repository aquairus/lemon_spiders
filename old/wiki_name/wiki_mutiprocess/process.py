#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import requests 
from requests import ConnectionError
import sys
from bs4 import BeautifulSoup
import re
import time
from multiprocessing.dummy import Pool
import Queue
from time import sleep



reload(sys)
sys.setdefaultencoding( "utf-8" )

scale=3
debug=1


delay =0.5
pre_url="https://zh.wikipedia.org"

pool = Pool(8)


def get_children(url):
	try:
		r = requests.get(url)
		text=r.text
	except BaseException, e:
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	childen=[]
	for child in soup.find_all('a',class_="CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory"):
		childen.append(pre_url+child.get("href"))
	return childen


def get_names(url):
	try:
		r = requests.get(url)
		text=r.text
	except ConnectionError, e:
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	names=[]
	for item in soup.find_all('div',class_="mw-category-group")[:-2]:
		names.append(item.ul.li.a.text)
	return names

def p_t():
	print time.time()-start_time





def new_category(url):
	return category(url)


class category():
	def __init__(self, url):
		self.url = url 
		self.child_urls =get_children(url)
		self.names=[]

		if not self.child_urls:
			#print "get a leave"
			self.names=get_names(url)
			self.print_names()
			self.write_names(wiki_of)
			#print "finish a leave"
		else:
			#print "get a node"
			for i in self.child_urls[:scale]:
				urlqueue.put(i)

	def print_names(self):
		for name in self.names:
			print name

	def write_names(self,of):
		for name in self.names:
			of.write(name+"\n")



	


pre_url="https://zh.wikipedia.org"
test_url="https://zh.wikipedia.org/wiki/Category:日本的大學教師"
test2_url="https://zh.wikipedia.org/wiki/Category:各國政治人物"
start_url="https://zh.wikipedia.org/wiki/Category:按國籍分類"

wiki_of =open('process.txt','w+')

urlqueue=Queue.LifoQueue()
start_time=time.time()

start_time=time.time()
root=category(start_url)

while not urlqueue.empty():
 	pool.apply(new_category, (urlqueue.get(),))
 	sleep(delay)

pool.close()
pool.join()
print time.time()-start_time
print "All subprocesses done."
wiki_of.close()

# def get_info(url):
# 	r = requests.get(url)
# 	print r.text
# 	print r.encoding 

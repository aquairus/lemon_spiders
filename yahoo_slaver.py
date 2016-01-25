#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import redis
import threadpool
import logging
from bs4 import BeautifulSoup
import requests
from time import sleep
import sys
import Queue
reload(sys)

slave_num=2
ques_time=100
sys.setdefaultencoding( "utf-8" )
master="spider01"
r_port=6369
delay=1




fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }
pre_url="https://answers.yahoo.com"


def get_arg():
	delay=1
	slave_NO=0
	try:
		options,args = getopt.getopt(sys.argv[1:],"hd:n:",["help","dalay=","num="])
	except getopt.GetoptError:
		sys.exit()

	for name,value in options:
		if name in ("-h","--help"):
			print "usage:\n  --dalay\n  \--capacity"
			sys.exit()
		if name in ("-d","--dalay"):
			print 'delay is----',value
			dalay=float(value)
		if name in ("-n","--num"):
			print 'number is----',value
			slave_NO=value
	filename="../yahoo_"+str(slave_NO)+".txt"
	task_url="task_url"+str(slave_NO)


def get_soup(url):
    try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8"
		text=r.text
    except BaseException, e:
		print e
		sleep(delay)
		text=""
    return BeautifulSoup(text,"lxml")


def find_answer(soup):
    ansList=soup.find_all('span',class_="ya-q-full-text")
    all_ans=[]
    for ans in ansList:
		all_ans.append(ans.text)
    try:
		next=soup.find_all(id="ya-qn-pagination")[0]\
		.find_all('a',class_="Clr-bl")[-1]
    except BaseException, e:
		return	all_ans,None

    if next.text==" next":
		return all_ans,next.get('href')
    else:
		return all_ans,None


def find_relateQ(soup):
    qList=soup.find_all('div',class_="qTile Px-14 Py-8 Bgc-w")
    relateQ=[]
    for q in qList[:-1]:
        a=q.find("a")
        href=a.get("href")
        relateQ.append(href)
    return relateQ


def find_title(soup):
	title=soup.find("h1").text.lstrip().rstrip()
	return title

def find_Qa(soup):
	Qa={}
	Qa["content"]=find_title(soup)
	Qa["review"]=""
	all_ans,next=find_answer(soup)
	for ans in all_ans:
		Qa["review"]=Qa["review"]+ans+"<p>"

	while next:
		sleep(delay)
		next_soup=get_soup(pre_url+next)
		all_ans,next=find_answer(next_soup)
		for ans in all_ans:
			Qa["review"]=Qa["review"]+ans+"<p>"

	return Qa



def slave_work(url):
	soup=get_soup(url)
	relateQ=find_relateQ(soup)
	for Q in relateQ:
	fresh_Q.put(relateQ)
	Qa=find_Qa(soup)
	yh_of.write(json.dumps(Qa)+"\n")


def commit_answer(Qa):
    pass


class worker():
	def __init__(task_url,r,size=100*slave_num):
		self.task_k=task_url
		self.commit_k="fresh_url"
		self.r=r
		self.size=size

	def fetch_link(self,key=self.task_k,count=5):
		url_Queue=self.r.lrange(key,0,count-1)
		self.r.ltrim(key,count,-1)
		for Q in url_Queue:
			task_Q.put(Q)

	def commit_link(self,key=self.commit_k,new_Qlist):
		if self.length(key)<self.size:
			pipe=self.r.pipeline()
			for Q in new_Qlist:
				pipe.rpush(key,Q)
			pipe.execute()
		else:
			task_Q.put(new_Qlist)


	def length(self,key):
		return self.r.llen(key)


get_arg()
yh_of=open(filename)
if __name__ == '__main__':

	r = redis.StrictRedis(host=master, port=r_port,db=0)
	slaver=work(task_url,r)
	task_Q=Queue.Queue()
	fresh_Q=Queue.Queue()
	pool = threadpool.ThreadPool(thread_cnt)
	pool.wait()

	while not task_Q.empty():
		work = threadpool.WorkRequest(slave_work, task_Q.get())
		pool.putRequest(work)
		if tasl_Q.qsize()<ques_time:
			slaver.fetch_link()
		slaver.commit_link()
		sleep(delay)

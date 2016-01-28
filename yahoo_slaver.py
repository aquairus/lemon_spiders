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
import  getopt
import json
from tool import prog_bar,mail
import os
reload(sys)

sla_cnt=5
ques_time=100
sys.setdefaultencoding( "utf-8" )
master="spider01"
r_port=6369
delay=1

thread_cnt=16
roll_time=0.5

error_cnt=0
error_delay=10


fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }
pre_url="https://answers.yahoo.com"


def get_arg():
	delay=1
	slave_NO=0
	curren_f=0
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


	return slave_NO,curren_f,delay


def get_soup(url):
    try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8"
		text=r.text
    except BaseException, e:
		onerror(e)
		text=""
    return BeautifulSoup(text,"lxml")

def onerror(e):
	error_cnt+=1
	if error_cnt>40:
		sleep(error_delay*10)
	sleep(error_delay)
		# try:
		# 	mailbox=mail.mailbox(os.environ["mailuser"],os.environ["passwd"])
		# 	mailbox.send_msg(sys.argv[0],str(e))
		# except BaseException, e:

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

	soup=get_soup(pre_url+url)
	relateQ=find_relateQ(soup)
	fresh_Q.put(relateQ)
	Qa=find_Qa(soup)
	yh_of.write(json.dumps(Qa)+"\n")
	sleep(delay)




class worker():
	def __init__(self,r,sla_cnt):
		self.task_k="task_url"
		self.commit_k="fresh_url"
		self.r=r
		self.size=sla_cnt*100
		self.c_cnt=0
		self.f_cnt=0

	def unfinished(self):
		unfinished=self.r.llen(self.task_k)+self.r.llen(self.commit_k)
		return 	unfinished>0

	def init_work(self):
		while self.r.llen(self.task_k)<20:
			sleep(2)
		self.fetch_link()
		slave_work(task_Q.get())

	def fetch_link(self,count=20):
		url_Queue=self.r.lrange(self.task_k,0,count-1)
		self.r.ltrim(self.task_k,count,-1)
		for Q in url_Queue:
			task_Q.put(Q)
		self.f_cnt+=1

	def commit_link(self,new_Qlist):
		pipe=self.r.pipeline()
		for Q in new_Qlist:
			pipe.rpush(self.commit_k,Q)
		pipe.execute()
		self.c_cnt+=1



if __name__ == '__main__':
	bar=prog_bar.prog_bar(100)

	slave_NO,curren_f,delay=get_arg()

	filename="../yahoo_"+str(slave_NO)+str(curren_f)+".txt"
	yh_of=open(filename,'a+')

	r = redis.StrictRedis(host=master, port=r_port,db=0)
	slaver=worker(r,sla_cnt)
	task_Q=Queue.Queue()
	fresh_Q=Queue.Queue()
	pool = threadpool.ThreadPool(thread_cnt)
	slaver.init_work()


	while slaver.unfinished:
		task=task_Q.get()
		job = threadpool.WorkRequest(slave_work,(task,))
		pool.putRequest(job)

		if task_Q.qsize()<ques_time:
			slaver.fetch_link()

		if not fresh_Q.empty():
			slaver.commit_link(fresh_Q.get())

		if os.path.getsize(filename)>100000000:
			curren_f+=1
			filename="../yahoo_"+str(slave_NO)+str(curren_f)+".txt"
			yh_of=open(filename,'a+')
			bar.new_page(5)

		bar.reflash_r(slaver.f_cnt,task_Q.qsize(),slaver.c_cnt,curren_f,filename,error_cnt)
		sleep(roll_time)

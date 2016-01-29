#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import requests
from requests import ConnectionError
import sys
from bs4 import BeautifulSoup

import time
import threadpool
import Queue
from time import sleep
import os
from pybloom import BloomFilter
import  getopt
import cPickle as pickle
from tool import prog_bar,mail
import redis
import json
import random

reload(sys)
sys.setdefaultencoding( "utf-8" )


sla_cnt=5
salve_job=4000

thread_cnt=16
ques_time=500

start_p=2
end_p=100
total_p=end_p-start_p+2
roll_time=0.2
relay_time=5

start_url="https://answers.yahoo.com"
pre_url="https://answers.yahoo.com"

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }



filtername='../quesFilter'


def get_arg():
	delay =1
	urlcapacity=5000000
	try:
		options,args = getopt.getopt(sys.argv[1:],"hd:c:s:",["help","dalay=","capacity="])
	except getopt.GetoptError:
		sys.exit()

	for name,value in options:
		if name in ("-h","--help"):
			print "usage:\n  --dalay\n  \--capacity"
			sys.exit()
		if name in ("-d","--dalay"):
			print 'delay is----',value
			dalay=float(value)
		if name in ("-c","--capacity"):
			print 'capacity is----',value
			urlcapacity=int(value)

	return delay,urlcapacity

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


def get_next_q(cpos,bpos,sid=None):
	if not sid:
		url="https://answers.yahoo.com/_module?name=YANewDiscoverTabModule&after=pc"+\
	str(cpos*20-20)+"~p%3A0&disableLoadMore=false&bpos="+str(bpos)+"&cpos="+str(cpos)
	else:
		url="https://answers.yahoo.com/_module?name=YANewDiscoverTabModule&after=pc"+\
	str(cpos*20-20)+"~p%3A0&sid="+sid+"&disableLoadMore=false&bpos="+str(cpos*20-20)+"&cpos="+str(cpos)

	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8"
		text=r.text

	except BaseException, e:

		print e
		sleep(delay)
		text=""

	text_html=json.loads(text)["YANewDiscoverTabModule"]["html"]

	soup = BeautifulSoup(text_html,"lxml")
	Qlist=[]
	for h3 in soup.find_all("h3"):
		href=h3.a.get("href")
		Qlist.append(href)
	return Qlist



def get_question(url):
	soup = get_soup(url)
	questionList=soup.find_all('a',class_="Fz-14 Fw-b Clr-b Wow-bw title")
	first_list=[]
	for q in questionList:
		href=q.get("href")
		first_list.append(href)

	sid_list=[]
	sids=soup.find_all('a',class_=" Mstart-3 unselected D-ib")[1:]
	for item in sids:
		sid_list.append(item.get("href")[15:])

	return first_list,sid_list


def ques_factory(cpos):
	q_list=get_next_q(cpos,cpos*19-17)
	for sid in sids:
		q_list=q_list+get_next_q(cpos,0,sid)
	return q_list


def init_filter(urlcap):
	try:
		blf_file=open(filtername,'r')
		q_filter=pickle.load(blf_file)
		blf_file.close()
		print "continue my work"
		return q_filter,1

	except BaseException, e:
		print "new fileter"
		q_filter = BloomFilter(capacity=urlcap,error_rate=0.001)
		return q_filter,0


def start_working(start_p,end_p,relay):

	cpos_l=range(start_p,end_p)
	if relay:
		print "relay"
		random.shuffle(cpos_l)
		ques_works=threadpool.makeRequests(ques_factory,cpos_l,url_Q.r_pour)
		for i in range(relay_time):
			pool.putRequest(ques_works.pop())
		bar.new_page(relay_time)
		pool.wait()
	else:
		ques_works=threadpool.makeRequests(ques_factory,cpos_l,url_Q.r_pour)
		pool.putRequest(ques_works.pop())
		pool.wait()

	return ques_works


class url_Queue():

	def __init__(self,Q_filter):
		self.filter=Q_filter
		self.Q=Queue.Queue()

	def add(self,href):
		if not href in self.filter:
			self.filter.add(href)
			self.Q.put(href)

	def length(self):
		return len(self.filter)

	def r_pour(self,req,links):
		for link in links:
			self.add(link)

	def pour(self,links):
		for link in links:
			self.add(link)


class scheduler():
	def __init__(self,r,sla_cnt,size=100):
		self.r=r
		self.step=60*sla_cnt
		self.slave=sla_cnt
		self.size=size
		self.out_q=0
		self.in_q=0

	def unfinished_cnt(self,q_size):
		return 	self.out_q+self.in_q+q_size

	def dist(self,key,q):
		self.out_q=self.length(key)

		if self.out_q<self.size*self.slave:
			pipe=self.r.pipeline()
			for s in xrange(self.step):
				if not q.Q.empty():
					task=q.Q.get()
					pipe.rpush(key,task)
			pipe.execute()

	def dist_all(self,key,q):
		for i in xrange(self.slave):
			self.dist(key,q)

	def retirve(self,key,q):
		self.in_q=self.length(key)

		fresh_url=r.lrange(key,0,self.step*self.slave-1)
		q.pour(fresh_url)
		r.ltrim(key,self.step*self.slave,-1)

	def function():
		pass

	def length(self,key):
		return self.r.llen(key)






if __name__ == '__main__':

	pool = threadpool.ThreadPool(thread_cnt)
	start_t=time.time()

	delay,urlcapacity=get_arg()

	Ques_f,relay=init_filter(urlcapacity)
	url_Q=url_Queue(Ques_f)

	r = redis.StrictRedis(host='spider01', port=6369, db=0)
	master=scheduler(r,sla_cnt,size=salve_job)
	bar=prog_bar.prog_bar(total_p)


	questions,sids=get_question(start_url)
	url_Q.pour(questions)
	ques_works=start_working(start_p,end_p,relay)


	while len(url_Q.filter)<urlcapacity:

		t=time.time()-start_t

		master.dist_all("task_url",url_Q)

		wait_q=url_Q.Q.qsize()
		bar.reflash(t,url_Q.length(),master.in_q,wait_q,master.out_q)

		if wait_q<ques_time*sla_cnt:
			master.retirve("fresh_url",url_Q)

		if int(t)%120==0:
			blf_file=open(filtername,'w')
			pickle.dump(url_Q.filter,blf_file)
			blf_file.close()

		sleep(roll_time)

		if wait_q<ques_time&len(ques_works)>0:
	 		bar.new_page(1)
	 		pool.putRequest(ques_works.pop())

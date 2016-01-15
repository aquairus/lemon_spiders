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
import json
import random
import os
from pybloom import BloomFilter



reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=16

delay =1
error_delay=1
pause=12
vocation=60
ques_time=100
start_p=2
end_p=100
urlcapacity=10000


exp = re.compile(ur'.*?·.*')
en_exp = re.compile(ur'.*?·.*')

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }
filename="../yahoo.txt"



def get_answer(url,ques):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text


	except BaseException, e:
		Ques_queue.put((url,ques))
		print e
		sleep(delay*error_delay)
		text=""
	soup = BeautifulSoup(text,"lxml")
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


def get_Qa(url,ques):
	Qa={}
	Qa["content"]=ques
	Qa["review"]=""

	all_ans,next=get_answer(pre_url+url,ques)
	for ans in all_ans:
		Qa["review"]=Qa["review"]+ans+"<p>"
	while next:
		sleep(delay)
		print "next"
		all_ans,next=get_answer(pre_url+next,ques)
		for ans in all_ans:
			Qa["review"]=Qa["review"]+ans+"<p>"
	yh_of.write(json.dumps(Qa)+"\n")
	print "--a Q&A"




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
		urlqueue.put(url)
		print e
		sleep(delay*error_delay)
		text=""
	
	text_html=json.loads(text)["YANewDiscoverTabModule"]["html"]

	soup = BeautifulSoup(text_html,"lxml")
	for h3 in soup.find_all("h3"):

		href=h3.a.get("href")
		Ques_queue.put((href,h3.a.text))
		print href
		#print h3.a.text
		if not href in ques_filter:
			ques_filter.add(href)
			print href
			Ques_queue.put((href,h3.a.text))
		else:
			print "-----repeat"	
	



def get_question(url):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text


	except BaseException, e:
		urlqueue.put(url)
		print e
		sleep(delay*error_delay)
		text=""

	soup = BeautifulSoup(text,"lxml")
	
	questionList=soup.find_all('a',class_="Fz-14 Fw-b Clr-b Wow-bw title")
	for q in questionList:
		Ques_queue.put((q.get("href"),q.text))
	sids=soup.find_all('a',class_=" Mstart-3 unselected D-ib")
	for item in sids:
		sid_list.append(item.get("href")[15:])
		#print item.get("href")[15:]




def ques_factory(cpos):
	get_next_q(cpos,cpos*19-17)
	for sid in sid_list:
		print sid
		get_next_q(cpos,0,sid)

	print "lots of new pages"



start_url=["https://answers.yahoo.com"]

test_url=["https://answers.yahoo.com/question/index?qid=20160111033016AA5vIfQ"]
test_url2=["https://answers.yahoo.com/question/index?qid=20160110150611AAtKxgF"]
pre_url="https://answers.yahoo.com"


yh_of =open(filename,'w+')

Ques_queue=Queue.LifoQueue()
urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt) 
start_time=time.time()
ques_filter = BloomFilter(capacity=urlcapacity,error_rate=0.001)
sid_list=[]



if __name__ == '__main__':
	get_question(start_url[0])

	cpos_list=range(start_p,end_p)

	ques_works=threadpool.makeRequests(ques_factory,cpos_list)
	#print type(ques_works)
	print "qa start "

	while not Ques_queue.empty():
		data=Ques_queue.get()
		work = threadpool.WorkRequest(get_Qa, data)
		pool.putRequest(work) 

		if Ques_queue.qsize()<ques_time&len(ques_works)>0:
	 		print "-------adding------"
	 		print os.path.getsize(filename)
	 		print len(ques_filter)
	 		pool.putRequest(ques_works.pop())
	 		pool.wait()

	 	sleep(delay)
	 	t=time.time()-start_time
	 	if int(t)%pause==0:
			print "-------sleep------"
	 		print os.path.getsize(filename)
	 		print len(ques_filter)
	 		print "----sleep------"

	 		sleep(random.randint(vocation/4,vocation))



	pool.wait()
	print Ques_queue.qsize()
	print "\n\n\n\n\n "
	print "finish "


yh_of.close()


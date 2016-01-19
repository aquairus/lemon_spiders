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
import  getopt
import cPickle as pickle


reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=16

delay =0.5	#vps:0.5  #ubuntu:0.8
page_delay=10
error_delay=10

pause=80
vocation=40
ques_time=200

start_p=2
end_p=100

urlcapacity=5000
slience=False


exp = re.compile(ur'.*?·.*')
en_exp = re.compile(ur'.*?·.*')

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }


filename="../naver.txt"
logname="../naver_log.txt"
filtername="../naver_quesFilter"



def get_answer(url):
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
	title=soup.find('h3',class_="_endTitleText").text.lstrip().rstrip()
	ansList=soup.find_all('div',class_="_endContentsText")
	all_ans=[]

	for ans in ansList[1:]:
		all_ans.append(ans.text)
	return title,all_ans


def get_relateQ(url):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text

	except BaseException, e:
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	qList=soup.find('ul',class_="aside_list").find_all("a")
	for q in qList:
		if not href in ques_filter:
			ques_filter.add(href)



def get_Qa(url):
	Qa={}
	Qa["review"]=""
	if Ques_queue.qsize()<ques_time:
		get_relateQ(pre_url+url)
	ques,all_ans=get_answer(pre_url+url)

	for ans in all_ans:
		Qa["review"]=Qa["review"]+ans+"<p>"
	Qa["content"]=ques
	yh_of.write(json.dumps(Qa, ensure_ascii=False)+"\n")


	

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
	
	questionList=soup.find_all('td',class_="title")

	for q in questionList:
		href=q.a.get("href")
		if not href in ques_filter:
			ques_filter.add(href)
			Ques_queue.put(href)


def ques_factory(page):

	for dirId in range(1,13):
		url="http://kin.naver.com/qna/list.nhn?m=kinup&dirId="+str(dirId)+\
		"&queryTime=2016-01-19+15%3A39%3A54&page="+str(page)
		sleep(delay)
		get_question(url)
	print "new page " 


def get_arg():
	try:
		options,args = getopt.getopt(sys.argv[1:],"hd:c:s:",["help","dalay=","capacity=","slience"])
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
			urlcapacity=float(value)
		if name in ("-s"):
			print "slience mode"
			slience=True

	if slience:
		yahoo_log=open(logname,'w')
		old=sys.stdout 
		sys.stdout=yahoo_log  


def init_filter(url_c):		
	try:
		blf_file=open(filtername,'r')
		q_filter=pickle.load(blf_file)
		blf_file.close()
		return q_filter
	except BaseException, e:
		print "a new filter "
		q_filter = BloomFilter(capacity=url_c,error_rate=0.001)
		return q_filter


start_url=["https://answers.yahoo.com"]

test_url="http://kin.naver.com/qna/detail.nhn?d1id=11&dirId=110408&docId=243351741"
test_url2="http://kin.naver.com/qna/list.nhn?m=kinup&dirId=5"
pre_url="http://kin.naver.com"




get_arg()

yh_of =open(filename,'w+')

urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt) 
start_time=time.time()
sid_list=[]
Ques_queue=Queue.Queue()

ques_filter=init_filter(urlcapacity)

if __name__ == '__main__':

	ques_factory(1)

	cpos_list=range(start_p,end_p)

	ques_works=threadpool.makeRequests(ques_factory,cpos_list)

	print "start scrawing "

	while not Ques_queue.empty():
		data=Ques_queue.get()

		work = threadpool.WorkRequest(get_Qa, (data,))
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
	 		sys.stdout.flush()
	 		if int(t)%21==0:
	 			blf_file=open(filtername,'w')
				pickle.dump(ques_filter,blf_file)
				blf_file.close()


	 		sleep(random.randint(vocation/4,vocation))



	pool.wait()

	print "\n\n\n\n\n "
	print "finish "
	print "total question:"+str(len(ques_filter))
	print "data size:"+str(os.path.getsize(filename))
	print "time:"+str(t)



yh_of.close()

if slience:
	sys.stdout=old 	
	yahoo_log.close() 

blf_file=open(filtername,'w')
pickle.dump(ques_filter,blf_file)
blf_file.close()

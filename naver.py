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
import mail
from progressive.bar import Bar


reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=16

delay =0.4	#vps:0.4  #ubuntu:0.8
page_delay=10
error_delay=10

pause=50
vocation=40
ques_time=200

start_p=1
end_p=100
total_p=end_p-start_p+1

urlcapacity=80000
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
		print e
		sleep(delay*error_delay)
		text=""

	soup = BeautifulSoup(text,"lxml")
	try:
		title=soup.find('h3',class_="_endTitleText").text.lstrip().rstrip()
	except BaseException, e:
		title=""
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
	try:
		qList=soup.find('ul',class_="aside_list").find_all("a")
		for q in qList:
			href=q.get("href")

			if not href in ques_filter:
				if "/qna/" in href:
					ques_filter.add(href)

	except BaseException, e:
			pass


def get_Qa(url):
	Qa={}
	Qa["review"]=""
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

def get_expert_q(url):

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

	ulList=soup.find_all('ul',class_="list_qna")

	for ul in ulList:
		alist=ul.find_all("a")
		for a in alist:
			href=a.get("href")
			if not href in ques_filter:
				ques_filter.add(href)
				Ques_queue.put(href)

def ques_factory(page):

	for dirId in range(1,13):

		kind="ing"
		url="http://kin.naver.com/qna/list.nhn?m="+kind+"&dirId="+str(dirId)+\
		"&queryTime=2016-01-19+15%3A39%3A54&page="+str(page)
		get_question(url)



		kind="directoryExpert"
		url="http://kin.naver.com/qna/list.nhn?m="+kind+"&dirId="+str(dirId)+\
		"&queryTime=2016-01-19+15%3A39%3A54&page="+str(page)

		get_expert_q(url)


		kind="kinup"
		url="http://kin.naver.com/qna/list.nhn?m="+kind+"&dirId="+str(dirId)+\
		"&queryTime=2016-01-19+15%3A39%3A54&page="+str(page)
		get_question(url)

		sleep(delay)



def init_filter(url_c):
	try:
		blf_file=open(filtername,'r')
		q_filter=pickle.load(blf_file)
		blf_file.close()
		return q_filter,open(filename,'a'),1
	except BaseException, e:
		print "a new filter "
		q_filter = BloomFilter(capacity=url_c,error_rate=0.001)
		return q_filter,open(filename,'w+'),0


def show_stat(cursor,s_mode):
	if not s_mode:
 		bar.cursor.restore()  # Return cursor to start
		bar.draw(value=cursor)

	print "size:"+str(os.path.getsize(filename))
	print "filter:"+str(len(ques_filter))
	print "spent: "+str(t/60)+" mins"
	print "rest: "+str(t/cursor*(total_p-cursor)/60)+" mins"
	sys.stdout.flush()




test_url="http://kin.naver.com/qna/detail.nhn?d1id=11&dirId=110408&docId=243351741"
test_url2="http://kin.naver.com/qna/list.nhn?m=kinup&dirId=5"
pre_url="http://kin.naver.com"




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

ques_filter,yh_of,relay=init_filter(urlcapacity)

urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt)
start_time=time.time()

Ques_queue=Queue.Queue()


if slience:
	yahoo_log=open(logname,'w')
	old=sys.stdout
	sys.stdout=yahoo_log
else:
	bar = Bar(max_value=total_p)
	bar.cursor.clear_lines(7)
	bar.cursor.save()
	cursor=1
	bar.draw(value=cursor)




if __name__ == '__main__':

	cpos_list=range(start_p,end_p)

	if relay:
		random.shuffle(cpos_list)
		ques_works=threadpool.makeRequests(ques_factory,cpos_list)
	else:
		ques_works=threadpool.makeRequests(ques_factory,cpos_list)


	pool.putRequest(ques_works.pop())
	pool.wait()


	while not Ques_queue.empty():

		data=Ques_queue.get()
		work = threadpool.WorkRequest(get_Qa, (data,))
		pool.putRequest(work)

		t=time.time()-start_time
		if Ques_queue.qsize()<ques_time&len(ques_works)>0:
			print Ques_queue.qsize()
			print len(ques_works)
	 		pool.putRequest(ques_works.pop())
	 		cursor+=1
	 		show_stat(cursor,slience)


	 	sleep(delay)

	 	if int(t)%pause==0:
	 		if int(t)%3==0:
	 			blf_file=open(filtername,'w')
				pickle.dump(ques_filter,blf_file)
				blf_file.close()

	 		sleep(random.randint(vocation/4,vocation))



	pool.wait()

	final_msg="\n\n "+ "finish "\
	+ "total question:"+str(len(ques_filter))\
	+"data size:"+str(os.path.getsize(filename))+"time:"+str(t)
	print final_msg

	mailbox=mail.mailbox(os.env["mailuser"],os.env["passwd"])
	mailbox.send_msg(sys.argv[0],final_msg)

yh_of.close()

if slience:
	sys.stdout=old
	yahoo_log.close()

blf_file=open(filtername,'w')
pickle.dump(ques_filter,blf_file)
blf_file.close()

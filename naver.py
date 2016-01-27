#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import requests
import sys
from bs4 import BeautifulSoup
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
from tool import  prog_bar,mail


reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=16
vocation=20
ques_time=200

start_p=1
end_p=100
total_p=end_p-start_p+1

error_cnt=0
error_delay=10


fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }


filename="../naver.txt"
ft_name="../naver_quesFilter"
pre_url="http://kin.naver.com"



def get_arg():
	urlcapacity=80000
	delay =0.5 #vps:0.5  #ubuntu:0.8
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
		onerror(e)
		text=""
    return BeautifulSoup(text,"lxml")

def onerror(e):
	error_cnt+=1
	if error_cnt>40:
		mailbox=mail.mailbox(os.env["mailuser"],os.env["passwd"])
		mailbox.send_msg(sys.argv[0],str(e))

	sleep(error_delay)

def get_answer(url):
	soup = get_soup(url)
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
	soup = get_soup(url)
	try:
		qList=soup.find('ul',class_="aside_list").find_all("a")
	except BaseException, e:
		return

	for q in qList:
		href=q.get("href")
		if not href in q_filter:
			if "/qna/" in href:
				q_filter.add(href)
				Ques_queue.put(href)


def get_Qa(url):
	Qa={}
	Qa["review"]=""
	get_relateQ(pre_url+url)
	ques,all_ans=get_answer(pre_url+url)

	for ans in all_ans:
		Qa["review"]=Qa["review"]+ans+"<p>"
	Qa["content"]=ques
	nv_of.write(json.dumps(Qa, ensure_ascii=False)+"\n")

def get_question(url):
	soup = get_soup(url)
	questionList=soup.find_all('td',class_="title")

	for q in questionList:
		href=q.a.get("href")

		if not href in q_filter:
			q_filter.add(href)
			Ques_queue.put(href)

def get_expert_q(url):

	soup =get_soup(url)
	ulList=soup.find_all('ul',class_="list_qna")

	for ul in ulList:
		alist=ul.find_all("a")
		for a in alist:
			href=a.get("href")
			if not href in q_filter:
				q_filter.add(href)
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
		blf_file=open(ft_name,'r')
		q_filter=pickle.load(blf_file)
		blf_file.close()
		return q_filter,open(filename,'a')
	except BaseException, e:
		print "a new filter "
		q_filter = BloomFilter(capacity=url_c,error_rate=0.001)
		return q_filter,open(filename,'w+')



#
# test_url="http://kin.naver.com/qna/detail.nhn?d1id=11&dirId=110408&docId=243351741"
# test_url2="http://kin.naver.com/qna/list.nhn?m=kinup&dirId=5"
# pre_url="http://kin.naver.com"



def start_working(start_p,end_p,pool):
	cpos_list=range(start_p,end_p)
	random.shuffle(cpos_list)
	q_works=threadpool.makeRequests(ques_factory,cpos_list)
	pool.putRequest(q_works.pop())
	pool.wait()
	return q_works

if __name__ == '__main__':

	delay,urlc=get_arg()
	q_filter,nv_of=init_filter(urlc)

	urlqueue=Queue.LifoQueue()
	Ques_queue=Queue.Queue()
	pool = threadpool.ThreadPool(thread_cnt)
	start_time=time.time()

	bar = prog_bar.prog_bar(total_p)
	q_works=start_working(start_p,end_p,pool)



	while not Ques_queue.empty():

		data=Ques_queue.get()
		work = threadpool.WorkRequest(get_Qa, (data,))
		pool.putRequest(work)

		t=time.time()-start_time

		if Ques_queue.qsize()<ques_time&len(q_works)>0:
	 		pool.putRequest(q_works.pop())
			bar.new_page(1)

		bar.get_stat(len(q_filter),t,filename,error_cnt)
	 	sleep(delay)

	 	if int(t)%111==0:
 			blf_file=open(ft_name,'w')
			pickle.dump(q_filter,blf_file)
			blf_file.close()
	 		sleep(random.randint(vocation/4,vocation))

	pool.wait()

	mailbox=mail.mailbox(os.env["mailuser"],os.env["passwd"])
	mailbox.send_msg(sys.argv[0],"finished")

nv_of.close()

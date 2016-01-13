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



reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=16
delay =0.5
pause=50
vocation=20
start_p=2
end_p=100

exp = re.compile(ur'.*?·.*')
en_exp = re.compile(ur'.*?·.*')

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }



def get_answer(url,ques):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text


	except BaseException, e:
		Ques_queue.put((url,ques))
		print e
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
		all_ans,next=get_answer(pre_url+next,ques)
		for ans in all_ans:
			Qa["review"]=Qa["review"]+ans+"<p>"
	yh_of.write(json.dumps(Qa)+"\n")
	print "a Q&A"




def get_next_q(cpos,bpos,sid=None):
	if not sid:
		url="https://answers.yahoo.com/_module?name=YANewDiscoverTabModule&after=pc"+\
	str(cpos*20-20)+"~p%3A0&disableLoadMore=false&bpos="+str(bpos)+"&cpos="+str(cpos)
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text

	except BaseException, e:
		urlqueue.put(url)
		print e
		text=""
	
	text_html=json.loads(text)["YANewDiscoverTabModule"]["html"]

	soup = BeautifulSoup(text_html,"lxml")
	for h3 in soup.find_all("h3"):
		Ques_queue.put((h3.a.get("href"),h3.a.text))
		#print h3.a.get("href")
		#print h3.a.text
	print "a new page"



def get_question(url):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8" 
		text=r.text


	except BaseException, e:
		urlqueue.put(url)
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	
	questionList=soup.find_all('a',class_="Fz-14 Fw-b Clr-b Wow-bw title")
	for q in questionList:
		#print q.text
		Ques_queue.put((q.get("href"),q.text))



def ques_factory(stat,end):
	for cpos in range(start,end):
		get_next_q(cpos,cpos*19-17)
		sleep(delay)




start_url=["https://answers.yahoo.com"]

test_url=["https://answers.yahoo.com/question/index?qid=20160111033016AA5vIfQ"]
test_url2=["https://answers.yahoo.com/question/index?qid=20160110150611AAtKxgF"]
pre_url="https://answers.yahoo.com"


yh_of =open('../yahoo.txt','w+')

Ques_queue=Queue.LifoQueue()
urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt) 
start_time=time.time()





get_question(start_url[0])

work = threadpool.WorkRequest(ques_factory,(start_p,end_p))
pool.putRequest(work) 

print "qa start "

while not Ques_queue.empty():
	data=Ques_queue.get()
	work = threadpool.WorkRequest(get_Qa, data)
	pool.putRequest(work) 
 	sleep(delay)
 	t=time.time()-start_time
 	if int(t)%pause==0:
 		sleep(random.randint(vocation/2,vocation))
pool.wait()
print "\n\n\n\n\n "
print "finish "


yh_of.close()


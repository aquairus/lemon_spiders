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
#import mail

reload(sys)
sys.setdefaultencoding( "utf-8" )

thread_cnt=16

delay =0.8	#vps:0.8  #ubuntu:12
error_delay=10
pause=32
vocation=40
ques_time=100
start_p=2
end_p=100
urlcapacity=800000000
slience=False
t=0
relay_time=10

exp = re.compile(ur'.*?·.*')
en_exp = re.compile(ur'.*?·.*')

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }


filename="../../yahoo.txt"
log_name='../../yahoo_log.txt'
log_max=2000000
filtername='../../quesFilter'
cnt=0


def get_answer(url,ques):
	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8"
		text=r.text

	except BaseException, e:
		#get_Qa
		#Ques_queue.put((url,ques))
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


def get_relateQ(url):

	try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8"
		text=r.text

	except BaseException, e:
		print e
		text=""

	soup = BeautifulSoup(text,"lxml")
	qList=soup.find_all('div',class_="qTile Px-14 Py-8 Bgc-w")
	for q in qList[:4]:
		a=q.find("a")
		text=a.text
		href=a.get("href")
		##print text
		if not href in ques_filter:
			ques_filter.add(href)
			Ques_queue.put((href,text))
		#else:
		#	print "-----repeat"


def get_Qa(url,ques):
	Qa={}
	Qa["content"]=ques
	Qa["review"]=""
	if Ques_queue.qsize()<ques_time:
		get_relateQ(pre_url+url)
	all_ans,next=get_answer(pre_url+url,ques)

	for ans in all_ans:
		Qa["review"]=Qa["review"]+ans+"<p>"
	while next:
		sleep(delay)
		#print "next"
		all_ans,next=get_answer(pre_url+next,ques)
		for ans in all_ans:
			Qa["review"]=Qa["review"]+ans+"<p>"

	yh_of.write(json.dumps(Qa)+"\n")
	#print "--a Q&A"


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
		#print href
		#print h3.a.text
		if not href in ques_filter:
			ques_filter.add(href)
			Ques_queue.put((href,h3.a.text))
		#else:
		#	print "-----repeat"


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
		href=q.get("href")
		if not href in ques_filter:
			ques_filter.add(href)
			Ques_queue.put((href,q.text))

	sids=soup.find_all('a',class_=" Mstart-3 unselected D-ib")[1:]
	for item in sids:
		sid_list.append(item.get("href")[15:])
		#print item.get("href")[15:]


def ques_factory(cpos):
	get_next_q(cpos,cpos*19-17)
	for sid in sid_list:

		get_next_q(cpos,0,sid)

#	print "lots of new pages"

def init_filter():
	try:
		blf_file=open(filtername,'r')
		q_filter=pickle.load(blf_file)
		blf_file.close()
		print "continue my work"
		return q_filter,open(filename,'a+'),1

	except BaseException, e:
		print "new fileter"
		q_filter = BloomFilter(capacity=urlcapacity,error_rate=0.001)
		return q_filter,open(filename,'w+'),0

start_url=["https://answers.yahoo.com"]

test_url=["https://answers.yahoo.com/question/index?qid=20160111033016AA5vIfQ"]
test_url2=["https://answers.yahoo.com/question/index?qid=20160110150611AAtKxgF"]
pre_url="https://answers.yahoo.com"



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
	yahoo_log=open(log_name,'w')
	old=sys.stdout
	sys.stdout=yahoo_log


urlqueue=Queue.LifoQueue()
pool = threadpool.ThreadPool(thread_cnt)
start_time=time.time()
sid_list=[]
Ques_queue=Queue.Queue()



ques_filter,yh_of,relay=init_filter()


if __name__ == '__main__':


	get_question(start_url[0])
	cpos_list=range(start_p,end_p)

	if relay:
		print "relay"
		random.shuffle(cpos_list)
		ques_works=threadpool.makeRequests(ques_factory,cpos_list)
		for i in range(relay_time):
			pool.putRequest(ques_works.pop())
			pool.wait()
	else:
		ques_works=threadpool.makeRequests(ques_factory,cpos_list)




#	print "qa start "

	while not Ques_queue.empty():
		data=Ques_queue.get()
		work = threadpool.WorkRequest(get_Qa, data)
		pool.putRequest(work)

		if Ques_queue.qsize()<ques_time&len(ques_works)>0:
	 #		print "-------adding------"
	 		print os.path.getsize(filename)
	 		print len(ques_filter)
	 		pool.putRequest(ques_works.pop())

	 	sleep(delay)

	 	t=time.time()-start_time
	 	if int(t)%pause==0:
			#print "-------sleep------"
	 		print os.path.getsize(filename)
	 		print len(ques_filter)
	 		sys.stdout.flush()
	 		if int(t)%3==0:
	 			blf_file=open(filtername,'w')
				pickle.dump(ques_filter,blf_file)
				blf_file.close()
				if slience:
					if int(os.path.getsize(log_name))>log_max:
						error_msg="total question:"+str(len(ques_filter))+\
						"time:"+str(t)
						#mail.send_msg(sys.argv[0],"error:"+error_msg)
						sys.exit()

	 		sleep(random.randint(vocation/4,vocation))



	pool.wait()
	t=time.time()-start_time
	final_msg="\n\n "+ "finish "\
	+ "total question:"+str(len(ques_filter))\
	+"data size:"+str(os.path.getsize(filename))+"time:"+str(t)
	print final_msg


yh_of.close()



blf_file=open(filtername,'w')
pickle.dump(ques_filter,blf_file)
blf_file.close()

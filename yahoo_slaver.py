#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import redis
import threadpool
import logging
from bs4 import BeautifulSoup
import requests
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


delay=0.8

fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }
pre_url="https://answers.yahoo.com"

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
    rerelateQ=[]
    for q in qList[:-1]:
        a=q.find("a")
        href=a.get("href")
        rerelateQ.append(href)
    return rerelateQ


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
	#yh_of.write(json.dumps(Qa)+"\n")

def commit_link(arg):
    pass

def commit_answer(arg):
    pass

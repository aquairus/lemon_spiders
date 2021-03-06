# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


delay=3


dept_re=re.compile(r"12/dept1")
teacher_re=re.compile(r"teacherId")
ps_of=open("../../ps.txt","w+")



def get_url(regex):
	url_list=[]
	links=driver.find_elements_by_tag_name("a")
	for link in links:
		url=link.get_attribute("href")

		if url and regex.search(url):
			url_list.append(url)
			#print url
	return url_list

def get_teacher_info(url):
	t_info={}
	
	t_info["url"]=url
	name=driver.find_elements_by_xpath("//span[@class='TJtab01Mcon']//p")[0].text
	t_info["name"]=name.split(ur"：")[1] 
	# print name.split(ur"：")[1] 
	dept=driver.find_elements_by_xpath("//span[@class='TJtab01Mcon']//p")[2].text
	t_info["dept"]=dept.split(ur"：")[1] 
	# print t_info["dept"]
	vote=driver.find_element_by_id("in_Stab2").text
	vote=vote.split(ur"：")[0][3:-1]
	t_info["vote"]=vote
	# print vote

	comment_urls=set()
	for a in driver.find_elements_by_xpath("//div[@class='TJpage']//a"):
		comment_urls.add(a.get_attribute("href"))
	
	comments_list=[]

	for c_url in comment_urls:
		driver.get(c_url)
		for div in driver.find_elements_by_xpath("//span[@class='TJR_info']"):
			comment={}
			value=div.text.split("\n")
			course=value[0].split(ur"：")[3]
			comment["time"]=value[0].split(ur"：")[2][:-5].strip()
			comment["course"]=course.strip()
			comment["content"]=value[1]

			comments_list.append(comment)
	t_info["comments"]=comments_list
	ps_of.write(json.dumps(t_info, ensure_ascii=False)+"\n")





commends_text="/commend_all"
start_urls=["https://m.facebook.com/profile.php?v=friends&id=100005145335207"]




driver = webdriver.PhantomJS('phantomjs')
#driver=webdriver.Firefox()
# driver.get("http://www.xuebang.com.cn/teacherId62745"+commends_text)
# get_teacher_info()


for s_url in start_urls:
	driver.get(s_url)
	sleep(delay)
	print "init"

teacher_urls=[]
dept_urls=get_url(dept_re)


for d_url in dept_urls:
	driver.get(d_url)
	teacher_urls=teacher_urls+get_url(teacher_re)
	sleep(delay)
	print "dept"


teacher_urls=set(teacher_urls[1450:])

cnt =0
for t_url in teacher_urls:
	if cnt>2000:
		driver.get(t_url+commends_text)
		get_teacher_info(t_url)
		sleep(delay)
	cnt+=1
	print len(teacher_urls)-cnt

driver.close()





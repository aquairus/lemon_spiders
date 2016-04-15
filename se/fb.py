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
idy_delay=40

fid=re.compile(r"\?id=")
friends=re.compile(r"全部好友")
fb_of=open("../../fb.txt","w+")



arabic_name=[]
name_list=[]
black_list_1=["add"]
black_list_2=[chr(i) for i in range(97,123)]

def isban(word,bl):
    for a in bl:
        if a in word:
            return True
    return False

s_url="https://m.facebook.com/profile.php?v=friends&id=100005145335207"

def get_url(regex):
	url_list=[]
	links=driver.find_elements_by_tag_name("a")
	for link in links:
		url=link.get_attribute("href")	
		text=link.text
		if url and regex.search(url):
			if not isban(url,black_list_1):
				if not isban(text,black_list_2):
					print text
					arabic_name.append(text)
					url_list.append(url)
	return url_list

def get_friend(regex):
	#url_list=[]
	links=driver.find_elements_by_tag_name("a")
	for link in links:
		url=link.get_attribute("href")
		text=link.text
		if "全部好友" in text:
			driver.get(url)
			return True
	return False


#driver = webdriver.PhantomJS('phantomjs')
driver=webdriver.Firefox()
driver.get(s_url)
sleep(idy_delay)
name_list=name_list+get_url(fid)

while name_list:
	todo=name_list.pop()
	driver.get(todo)
	new_friend=get_friend(friends)
	if new_friend:
		while True:
			try:
				name_list=name_list+get_url(fid)
				driver.find_element_by_id("m_more_friends").click()
			except BaseException,e:
				break				
	print "node finish"	
	print len(arabic_name)
	print len(name_list)
	sleep(delay)


# friend=driver.find_elements_by_xpath("//span[@class='TJtab01Mcon']//p")[0].text






# def get_teacher_info(url):
# 	t_info={}
	
# 	t_info["url"]=url
# 	name=driver.find_elements_by_xpath("//span[@class='TJtab01Mcon']//p")[0].text
# 	t_info["name"]=name.split(ur"：")[1] 
# 	# print name.split(ur"：")[1] 
# 	dept=driver.find_elements_by_xpath("//span[@class='TJtab01Mcon']//p")[2].text
# 	t_info["dept"]=dept.split(ur"：")[1] 
# 	# print t_info["dept"]
# 	vote=driver.find_element_by_id("in_Stab2").text
# 	vote=vote.split(ur"：")[0][3:-1]
# 	t_info["vote"]=vote
# 	# print vote

# 	comment_urls=set()
# 	for a in driver.find_elements_by_xpath("//div[@class='TJpage']//a"):

# 		comment_urls.add(a.get_attribute("href"))

# 	comments_list=[]

# 	for c_url in comment_urls:
# 		driver.get(c_url)
# 		for div in driver.find_elements_by_xpath("//span[@class='TJR_info']"):
# 			comment={}
# 			value=div.text.split("\n")
# 			course=value[0].split(ur"：")[3]
# 			comment["time"]=value[0].split(ur"：")[2][:-5].strip()
# 			comment["course"]=course.strip()
# 			comment["content"]=value[1]

# 			comments_list.append(comment)
# 	t_info["comments"]=comments_list
# 	ps_of.write(json.dumps(t_info, ensure_ascii=False)+"\n")







# # driver.get("http://www.xuebang.com.cn/teacherId62745"+commends_text)
# # get_teacher_info()




# teacher_urls=[]
# dept_urls=get_url(dept_re)


# for d_url in dept_urls:
# 	driver.get(d_url)
# 	teacher_urls=teacher_urls+get_url(teacher_re)
# 	sleep(delay)
# 	print "dept"


# teacher_urls=set(teacher_urls[1450:])

# cnt =0
# for t_url in teacher_urls:
# 	if cnt>2000:
# 		driver.get(t_url+commends_text)
# 		get_teacher_info(t_url)
# 		sleep(delay)
# 	cnt+=1
# 	print len(teacher_urls)-cnt

# driver.close()





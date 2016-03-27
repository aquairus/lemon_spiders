#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from time import sleep


import threadpool
import logging
from bs4 import BeautifulSoup
import requests



fake_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'Accept-Encoding':'gzip'
				 }


def get_soup(url):
    try:
		r = requests.get(url,headers = fake_headers)
		r.encoding="utf-8"
		text=r.text
    except BaseException, e:
		text=""
		print "error"
    return BeautifulSoup(text,"lxml")


def write_case(soup):
	title=soup.find_all('h3')[0]
	print title.text
	content=soup.find(id='divFullText')
	print content.text[30:]


def case_work(url):

	soup=get_soup(url)
	write_case(soup)
	print url





case_list=[]


f = open("/Users/apple/desktop/test.txt", 'w+')



if __name__ == '__main__':
	browser = webdriver.Firefox()
	browser.set_page_load_timeout(30)
	browser.implicitly_wait(20)
	browser.set_script_timeout(20)

	pool = threadpool.ThreadPool(8)

	browser.get("http://www.pkulaw.cn/Case/")
	elem=browser.find_element_by_xpath(".//*[@id='columnLeft']/div[2]/div[1]/div/ul/li[2]/a")
	elem.send_keys("seleniumhq" + Keys.RETURN)
	sleep(5)

	elem=browser.find_element_by_xpath(".//*[@id='columnLeft']/div[2]/div[1]/div/ul/li[4]/a")
	elem.send_keys("seleniumhq" + Keys.RETURN)
	sleep(5)
	a=raw_input("?")
	elem=browser.find_element_by_xpath(".//*[@id='columnLeft']/div[2]/div[1]/div/ul/li[6]/a")
	elem.send_keys("seleniumhq" + Keys.RETURN)




	for j in range(1):
		links=browser.find_elements_by_xpath(".//a[@class='title']")
		for a in links:
			href=a.get_attribute("href")
			print href
			case_list.append(href)
			
			
		sleep(8)
		Next_Page=browser.find_elements_by_xpath("//input[@id='btnPageNext']")[0]
		Next_Page.click()	
	browser.quit()



	print "content"
	pool = threadpool.ThreadPool(8)

	for case in case_list:
		job = threadpool.WorkRequest(case_work,(case,))
		pool.putRequest(job)
		sleep(0.5)
	pool.wait()	
from selenium import webdriver
from time import sleep
import re

link_re = re.compile(r"(/\d+/\d+)")

driver=webdriver.Firefox()

driver.set_page_load_timeout(25)
driver.set_script_timeout(12)

#driver=webdriver.PhantomJS('phantomjs')
script_click="document.getElementById('MainContent_CatListingCtrl_divMore').click()"

url="http://www.masrawy.com/Autos/autos_news/section/375/"
cnt=0
urls=set()


try:
	driver.get(url)
except BaseException,e:	
	pass


cnt=0
try:
	while True:
		driver.execute_script(script_click)
		cnt+=1
		print cnt
		sleep(1)

except BaseException,e:
	print "orz"


sleep(20)
links=driver.find_elements_by_tag_name("a")
for a in links:
 	href=a.get_attribute("href")
 	if href and link_re.search(href):
 		urls.add(href)

print len(urls)


#link_re.search(href)
# p=driver.find_element_by_class_name("loaderGif")
# style=p.get_attribute("style")
# next_page=style=="display: none;"
# print next_page

# except BaseException,e:
#     next_page=None
#     print url
#     print "fail"

# while next_page:
# 	#print "hhah"
# 	.click()
# 	sleep(5)
# 	p=driver.find_element_by_class_name("loaderGif")
# 	style=p.get_attribute("style")
# 	next_page=style=="display: none;"


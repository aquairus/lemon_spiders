import pymongo
from pymongo import MongoClient
import json
import sys
from time import sleep
reload(sys)
sys.setdefaultencoding( "utf-8" )
print "name?"
name=raw_input()


#name="ar3"
client = MongoClient()
client = MongoClient('spider08', 27017)
db = client.ar

yahoo=db.get_collection(name)



duplicate=set() 
cnt=0

f =open ("../../"+name+".txt","w+")

cursor=yahoo.find()
for line in cursor:
	line.pop("_id")
	url=line["url"]

	if not url in duplicate:
		f.write(json.dumps(line, ensure_ascii=False)+"\n")
	else:
		print "different"	

	duplicate.add(url)
	
	print "set:"+str(len(duplicate))
	cnt+=1
	print cnt
	
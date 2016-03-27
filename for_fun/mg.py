import pymongo
from pymongo import MongoClient
import json
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )
print "name?"
name=raw_input()


#name="ar3"
client = MongoClient()
client = MongoClient('spider05', 27017)
db = client.ar

yahoo=db.get_collection(name)




cnt=0

f =open ("../../"+name+".txt","w+")

cursor=yahoo.find()
for line in cursor:
	#f.write(json.loads(line)+"\n")
	line.pop("_id")
	#print line	
	#string=json.dumps(line, ensure_ascii=False)
	f.write(json.dumps(line, ensure_ascii=False)+"\n")
	cnt+=1
	print cnt
	
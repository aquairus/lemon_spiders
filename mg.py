import pymongo
from pymongo import MongoClient
import json
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

client = MongoClient()
client = MongoClient('spider08', 27017)
db = client.xm
yahoo = db.xm0



cnt=0

f =open ("../xm.txt","w+")

cursor=yahoo.find()
for line in cursor:
	#f.write(json.loads(line)+"\n")
	line.pop("_id")
	#print line	
	#string=json.dumps(line, ensure_ascii=False)
	f.write(json.dumps(line, ensure_ascii=False)+"\n")
	cnt+=1
	print cnt
	
import pymongo
from pymongo import MongoClient
import json
import sys
from time import sleep
reload(sys)
sys.setdefaultencoding( "utf-8" )

cnt=len(sys.argv)
print cnt


client = MongoClient("spider09", 27017)
db = client.cook


for name in  sys.argv[1:]:
	print name
	#print type(db)
	yahoo=db[name]
	duplicate=set()
	cnt=0

	f =open ("../../"+name+".txt","w+")

	cursor=yahoo.find()
	for line in cursor:
		line.pop("_id")
		url=line["title"]

		if not url in duplicate:
			f.write(json.dumps(line, ensure_ascii=False)+"\n")
			duplicate.add(url)
		else:
			print "different"

		#duplicate.add(url)

		#print "set:"+str(len(duplicate))
		cnt+=1
		print cnt

	print "final"
	print "set:"+str(len(duplicate))
	print "count"+str(cnt)

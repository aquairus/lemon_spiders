print "name?"
name=raw_input()
space=3000

src=open(name+".txt","r+")
des=open(name+"_0"+".txt","w+")

cnt=0
for line in src.readlines():
	cnt+=1
	if cnt%space==0:
		count=cnt/space
		print count
		des=open(name+"_"+str(count)+".txt","w+")
	des.write(line+"\n")

des.close()
src.close()



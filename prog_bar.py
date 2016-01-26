from progressive.bar import Bar
import os



class prog_bar(object):

    def __init__(self, total_p):
        self.cursor=1
        self.total=total_p
        self.bar = Bar(max_value=total_p)
        self.bar.cursor.clear_lines(7)
        self.bar.cursor.save()
        self.bar.draw(value=self.cursor)

    def new_page(self):
        self.cursor+=1

    def reflash(self,time,size):
        self.bar.cursor.restore()
        self.bar.draw(value=self.cursor)
    	print "filter:"+str(size)
        print "total "+str(size/self.cursor*self.total)
    	print "spent: "+str(time/60)+" min"
    	print "rest: "+str(time/self.cursor*(self.total-self.cursor)/60)+" min"

    def reflash_r(self,f_cnt,q_size,c_cnt,curren_f,filename,e_cnt):
        self.bar.cursor.restore()
        self.bar.draw(value=self.cursor)
    	print "fetch:"+str(f_cnt)
        print "q_size:"+str(q_size)
        print "commit: "+str(c_cnt)
    	print "curren_f: "+str(curren_f)
    	print "file_size: "+str(os.path.getsize(filename))
        print "error_count: "+str(e_cnt)

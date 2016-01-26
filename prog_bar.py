from progressive.bar import Bar
import os



class prog_bar(object):

    def __init__(self, total_p):
        self.cursor=1
        self.total=total_p
        self.bar = Bar(max_value=total_p)
        self.bar.cursor.clear_lines(10)
        self.bar.cursor.save()
        self.bar.draw(value=self.cursor)

    def new_page(self,cnt):
        self.cursor+=cnt

    def reflash(self,time,size,in_q,wait_q,out_q):
        self.bar.cursor.restore()
        self.bar.draw(value=self.cursor)
    	print "done:"+str(size)
        print "in_q:"+str(in_q)
        print "wait_q:"+str(wait_q)+"     out_q:"+str(out_q)
    	print "spent: "+str(int(time/60))+" min"
    	print "rest: "+str(int(time/self.cursor*(self.total-self.cursor)/60))+" min"


    def reflash_r(self,f_cnt,q_size,c_cnt,curren_f,filename,e_cnt):
        self.bar.cursor.restore()
        self.bar.draw(value=self.cursor)
        print "\n"
    	print "fetch:"+str(f_cnt)
        print "q_size:"+str(q_size)
        print "commit: "+str(c_cnt)
    	print "curren_f: "+str(curren_f)
    	print "file_size: "+str(os.path.getsize(filename))
        print "error_count: "+str(e_cnt)

    def get_stat(self,done,time,filename,e_cnt):
        f_size=os.path.getsize(filename)
        self.bar.cursor.restore()
        self.bar.draw(value=self.cursor)
        print "done: "+str(done)+"     file_size: "+str(int(f_size))
        print "total_size: "+str(int(f_size/self.cursor*(self.total-self.cursor)/60))
    	print "spent: "+str(int(time/60))+" min"
    	print "rest: "+str(int(time/self.cursor*(self.total-self.cursor)/60))+" min"
        print "error_count: "+str(e_cnt)

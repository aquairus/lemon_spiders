from progressive.bar import Bar



class prog_bar(object):

    def __init__(self, total_p):
        self.cursor=1
        self.total=total_p
        self.bar = Bar(max_value=total_p)
        self.bar.cursor.clear_lines(7)
        self.bar.cursor.save()
        self.bar.draw(value=self.cursor)

    def new_page(self,time,size):
        self.cursor+=1
        self.reflash(time,size)

    def reflash(self,time,size):
        self.bar.cursor.restore()
        self.bar.draw(value=self.cursor)
    	print "filter:"+str(size)
        print "total "+str(size/self.cursor*self.total)
    	print "spent: "+str(time/60)+" mins"
    	print "rest: "+str(time/self.cursor*(self.total-self.cursor)/60)+" mins"

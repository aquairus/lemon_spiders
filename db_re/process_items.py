#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import redis
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

class DoubanPipeline():
    def __init__(self):
        self.of=open("../../douban.txt",'w+')

    def save(self,item):

        item.pop("tid")
        item.pop("total")
        self.of.write(json.dumps(item, ensure_ascii=False)+"\n")



class mergePipeline(object):

    def __init__(self):
        self.content = dict()
        self.total = dict()
        self.answers=dict()



    def process_item(self,item):
        tid=item["tid"]

        if "total" in item:

            if item["total"]=="1":
                print "short topic"
                return item
            else:
                self.content[tid]=item.copy()
                self.total[tid]=item["total"]
            return

        if not tid in self.answers:
            self.answers[tid]={}

        pid=int(item["pid"])

        self.answers[tid][pid]=item["answers"]
        keys=self.answers[tid].keys()


        if not tid in self.total:
            return

        if len(keys)+1==int(self.total[tid]):
            for (v,c) in self.answers[tid].items():
                self.content[tid]["answers"]=\
                self.content[tid]["answers"]+c
            douban=self.content[tid]
            
            self.total.pop(tid)
            self.answers.pop(tid)
            self.content.pop(tid)
            print "long!!"
            return douban



def main():
    r = redis.Redis(host='spider03', port=6379,)
    doubanpp= DoubanPipeline()
    mergepp=mergePipeline()


    while True:
        # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
        source,data = r.blpop(["douban:items"])
        item = json.loads(data)

        item=mergepp.process_item(item)
        if item:
            doubanpp.save(item)

        #item = json.loads(data)
        # try:
        #     print u"Processing: %(name)s <%(link)s>" % item
        # except KeyError:
        #     print u"Error procesing: %r" % item


if __name__ == '__main__':

    main()

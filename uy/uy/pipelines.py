# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )


class uyPipeline(object):
    def open_spider(self, spider):
        self.of=open("../../"+spider.name+".txt",'w+')

    def process_item(self, item, spider):
        dic=dict(item)
        dic["type"]="news"
        self.of.write(json.dumps(dic, ensure_ascii=False)+"\n")

    def close_spider(self, spider):
        self.of.close()


class mergePipeline(object):

    def __init__(self):
        self.content = dict()
        self.total = dict()
        self.answers=dict()


    def process_item(self, item, spider):
        tid=item["tid"]

        if "total" in item:
            if item["total"]=="1":
                print "short topic"
                return item
            else:
                self.content[tid]=item.copy()
                self.total[tid]=item["total"]
                raise DropItem("content")


        if not tid in self.answers:
            self.answers[tid]={}

        pid=int(item["pid"])
        self.answers[tid][pid]=item["answers"]

        keys=self.answers[tid].keys()

        if len(keys)+1==int(self.total[tid]):
            for (v,c) in self.answers[tid].items():
                self.content[tid]["answers"]=\
                self.content[tid]["answers"]+c
            douban=self.content[tid].copy()
            self.total.pop(tid)
            self.answers.pop(tid)
            self.content.pop(tid)
            print "long!!"
            return douban
        else:
            raise DropItem("answers")
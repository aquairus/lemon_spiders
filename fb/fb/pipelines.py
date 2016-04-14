# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from scrapy.exceptions import DropItem
import json

Alphabet=[chr(i) for i in range(97,123)]
def isenglish(word):
    for a in Alphabet:
        if a in word:
            return True
    return False

class emptyPipeline(object):
    def process_item(self, item, spider):

        if isenglish(item["name"]):
            raise DropItem("Duplicate tempry item ")
        else:
            return item

class fbPipeline(object):

    def open_spider(self, spider):
        self.of=open("../../fb.txt",'w+')

    def process_item(self, item, spider):
        self.of.write(json.dumps(dict(item), ensure_ascii=False)+"\n")

    def close_spider(self, spider):
        self.of.close()

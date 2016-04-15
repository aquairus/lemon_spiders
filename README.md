# lemon_spiders
>Python 爬虫实践

这段时间在[公司]("http://www.speechocean.com")实习,工作主要是用爬虫收集各种语言的语料。实习快结束了，我在这里些写点文档介绍一下爬虫的实现方案，以及到的用各种开源工具。

既是对工作的总结，也希望能给后来的同学提供一些参考。水平有限，欢迎指正。 

##101

这个repertory刚创建的时候。 我并没有采集数据的实际经验。因此老板给我给我布置了一些相对简单的练习任务：爬取新浪新闻 百度人名 wiki的人名，问答网站的问答。 
为了理解更深刻的理解爬虫的原理。这部分没有使用框架，而是自己实现整个爬取，遍历的逻辑。

设计这个逻辑的时候，我参考了这篇知乎回答[如何入门 Python 爬虫](https://www.zhihu.com/question/20899988/answer/24923424)

具体实现在101的目录下面，我在这里稍微介绍一下我用的库

* [requests](http://cn.python-requests.org/zh_CN/latest/)：网络请求库，比urllib更容易上手，会帮你解决很多gzip，编码之类的问题

  
* [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id40)元素选择器，用于解析html。比xpath选择器和css选择器更简单的api。据说性能会差一点。


* [python-bloomfilter](https://github.com/jaybaird/python-bloomfilter)基于各种hash算法的去重器，比set的性能好的多。可以用于打


* [threadpool](http://chrisarndt.de/projects/threadpool/api/)一个简单的多线程任务队列

* re,json这些就没有什么好介绍的了。我还尝试过用email实现一个爬虫完成任务发邮件提醒自己的功能，和progressive展现爬虫进度的功能。然并卵，这些功能很鸡肋

##框架scrapy 
对爬虫有了一定了解以后，就可以试试框架了。省时省力。

Scrapy是python下最流行的爬虫框架。
下面是scrapy的架构概览。大概的描述了scrapy的数据流向。

![404](https://github.com/aquairus/lemon_spiders/blob/master/doc/scrapy_architecture.png)

* spider用于分析链接，生成请求，提取数据。

* scheduler用于调度任务队列。

* downloader用于发送请求。

* pipeline用于整理数据，储存数据。

一般来说我们只要在spider文件里面指定follow的链接，采集的链接，采集的字段。

在pipline里面指定储存方案。在setting里面设置delay，user-agent，cookie_enable之类的参数。就可以完成一个简单的爬虫了了。  

如果能满足需求的话建议继承CrawlSpider这个爬虫类。编写一条rule会比return 各种request 容易得多。

scrapy的文档相对来讲还是比较清晰的。但要深度定制的话可能还得看源码


详情请查看[中文文档](http://scrapy-chs.readthedocs.org/zh_CN/latest/intro/tutorial.html)和[源码](https://github.com/scrapy/scrapy)
##内容获取
###ajax
   现代的网站会使用各种各样的ajax技术，特别是评论功能和翻页功能，基本都是用ajax做的。对于看不懂JavaScript的爬虫来说xmlrequest是很不友好的。
   我们主要两种方法。   
   1.手工分析javascript。
	用web开发者工具 tamper data之类的工具抓包。找到api，然后请求这个api。
	2.selemiun
	selemiun是一个javascript库
    
##分布式
主从 完全分布式
    redis


[redis-py](https://github.com/andymccurdy/redis-py)

[scrapy-redis](https://github.com/rolando/scrapy-redis)


[mongodb](https://github.com/mongodb/mongo-python-driver)
##性能

##维护
   fabric(http://fabric-chs.readthedocs.org/zh_CN/chs/)
   
   supervisor(http://supervisor.readthedocs.org/en/stable/)
   
   ![404](https://github.com/aquairus/lemon_spiders/blob/master/doc/supervisord)

##Note

语料的抓取一般有去除html标签，但是保留<br><p>的要求。一开始我直接用re模块，把常用的标签都过滤掉。遇到新的

后来发现[blench](http://bleach.readthedocs.org/en/latest/) 这个库具有白名单的功能
  
# lemon_spiders
>Python 爬虫实践

这段时间在[公司]("http://www.speechocean.com")实习,工作主要是用爬虫收集各种语言的语料。实习快结束了，我在这里些写点文档介绍一下爬虫的实现方案，以及到的用各种开源工具。

既是对工作的总结，也希望能给后来的同学提供一些参考。水平有限，欢迎指正。 

##101

这个repository刚创建的时候。 我并没有采集数据的实际经验。因此老板给我给我布置了一些相对简单的练习任务：爬取新浪新闻 百度人名 wiki的人名，问答网站的问答。 
为了理解更深刻的理解爬虫的原理。这部分没有使用框架，而是自己实现整个爬取，遍历的逻辑。

设计这个逻辑的时候，我参考了这篇知乎回答[如何入门 Python 爬虫](https://www.zhihu.com/question/20899988/answer/24923424)

具体实现在101的目录下面，我在这里稍微介绍一下我用的库

* [requests](http://cn.python-requests.org/zh_CN/latest/)：网络请求库，比urllib更容易上手，会帮你解决很多gzip，编码之类的问题

  
* [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id40)元素选择器，用于解析html。比xpath选择器和css选择器更简单的api。据说性能会差一点。


* [python-bloomfilter](https://github.com/jaybaird/python-bloomfilter)基于各种hash算法的去重器，比set的性能好的多，占的空间也小。可以用于大规模的去重。


* [threadpool](http://chrisarndt.de/projects/threadpool/api/)一个简单的多线程任务队列

* re,json这些就没有什么好介绍的了。我还尝试过用email实现一个爬虫完成任务发邮件提醒自己的功能，和progressive展现爬虫进度的功能。然并卵，这些功能很鸡肋

##框架scrapy 
对爬虫有了一定了解以后，就可以试试框架了,省时省力。

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

scrapy的文档相对来讲还是比较清晰的。但要深入理解还得看源码


详情请查看[中文文档](http://scrapy-chs.readthedocs.org/zh_CN/latest/intro/tutorial.html)和[源码](https://github.com/scrapy/scrapy)
##内容获取
###ajax
   现代的网站会使用各种各样的ajax技术，特别是评论功能和翻页功能，基本都是用ajax做的。对于看不懂JavaScript的爬虫来说xmlrequest是很不友好的。
   我们主要两种方法。   

1.手工分析javascript。
	用web开发者工具 tamper data之类的工具抓包。找到api，然后直接从这个api里面取数据。这个方法的难度基本取决于api设计的复杂程度。太复杂就只能gg了
	
2.selemiun
	selemiun是一个javascript库,可以用于操纵本地的浏览器。模拟浏览器点击，填表之类的功能。调用selenium来进行翻页这样的操作。这个方法最大的缺点是慢。还有服务器上只能跑phantomjs。selenium对phantomjs的支持和firefox不太一样。调试起来还蛮麻烦的。

###遍历参数
有时候一些网站的页面很难顺着首页访问下去。
比如说新闻网站很久之前的新闻。或者一些被limit分页的查询。

这个时候我们可以考虑下面的做法
	
	pre_url="http://www.cookbooks.com/cookbooks_recipes/Recipe-Details.asp?id="
    for id in xrange(500000,1085642):
    	url=pre_url+str(id)
		yield Request(url,callback=self.parse_cook)
直接把所有的页面扫一遍。比去翻页，去设计爬取规则省事一些。

###yy
找网站的时候时不时会碰到这样的站点，很明显的sql注入漏洞。如果能获得数据库的权限就能直接去数据不用慢慢爬了。但对我也就想想罢了。具体操作还有很多我搞不定的技术问题，比如web防火墙。 
   ![404](https://github.com/aquairus/lemon_spiders/blob/master/doc/cook.png)  
###找语料
[similarsites](http://www.similarsites.com)
偶然间发现的一个站点。可以搜索和某网站A相似的所有站点。在找语料的时候蛮有帮助的。 
###反爬虫
根据UA，爬取速度进行的反爬虫都不是很难解决。但是需要登录，需要验证码的网站就搞不定了。有次想爬facebook。爬了一回就向我要图片验证码，过一会想我要短信验证码，最后还要身份证明。Orz搞不定   
##分布式
爬虫的爬取速度主要取决于，带宽和目标网站的响应速度。一台机器的带宽总是有限的，多台机器一起爬速度会快的多。可以用[redis](https://github.com/andymccurdy/redis-py)存放url，让多台机器共享任务

我在这里有两个尝试。

* 首先是在101这个目录下有个爬取yahoo问答的爬虫。yahoo_master负责分配任务，将去重后的url存到redis里面。yahoo_slaver负责从redis中读取去重后的url，访问网站解析页面，将新的url存到redis里。

这个方案有很多需要改进的地方。

首先是存储方案。我把爬取到的数据存在本地，最后发现爬完的时候很不好收集。[mongodb](https://github.com/mongodb/mongo-python-driver)是现在很流行的文档型数据库，支持json，支持分片。很适合爬虫的场景。

还有就是m/s的逻辑分开，代码不好维护


* 这个时候就可以看看现成的框架了。[scrapy-redis](https://github.com/rolando/scrapy-redis)是基于scrapy的一个插件。用scrapy-redis的调度器替换掉scrapy的的调度器。scrapy的downloade就会从redis中读取requests，scrapy的spider就会在提交redis的时候进行去重操作。安装好srapy-redis插件填上redis的地址和密码就可以进行分布式爬取了。

注意redis-server一定要加密码。一开始偷懒没设密码。结果服务器被就被黑掉了,黑客把redis清空，然后把自己的公钥写进了 ~/.ssh/authorized_key

![404](https://github.com/aquairus/lemon_spiders/blob/master/doc/key.PNG) 
                   
-----------------------------------redids crackit-----------------------------------
###性能
####io
在爬虫只有十几台的情况下，一台机子完全足够同时提供mongodb和redis-server的服务。如果规模再大一点的话可考虑分片。redis和mongodb都提供了分片功能。不过我在这里还没有试过。
####内存
* scrapy-redis会把requests存放在redis中，requests包含UA，cookie各种信息，占的空间还不小。100w条能占1g，如果requests的生成速度远大于消耗速度，可能会把内存用完然后机器就挂掉了。
* 在爬小说的时候，不同的小说章节是异步下载的。全部章节下载完了了才能存储。没有下载完的章节会留在内存里。留太多了也会gg。
* 内存问题可以通过提升配置，分片来解决

##部署
[fabric](http://fabric-chs.readthedocs.org/zh_CN/chs/)

fabric是python编写的基于ssh的运维工具，可以用简单的指令管理多台服务器。我在fabfile.py下写用于 开发机push代码，服务器同步代码，在新服务器上添加用户,安装依赖的脚本

添加一台vps的时候可以这样,安装scrapy,下载爬虫代码，写公钥

	def new_node(host):
		with settings(warn_only=True):
			run('apt-get install git -y')
			run('hostname '+host)
			run('adduser cxy')
			run('git clone https://github.com/aquairus/lemon_spiders.git \
				/home/cxy/lemon_spiders')
			run('source /home/cxy/lemon_spiders/conf/env.sh')
			run('cat /home/cxy/lemon_spiders/conf/spider_list >>/etc/hosts')



同步代码的时候可以用`fab update -P `一个命令在所有服务器上同步代码

	@roles('all')
	def update():
		with cd('/home/cxy/lemon_spiders'):
	 		run ("git reset --hard HEAD^^^")
	 		run("git pull")

   
[supervisor](http://supervisor.readthedocs.org/en/stable/)

supervisor是一个deamon的管理工具。比起nohup和screen来说多了远程管理功能和配置功能.比如我写了很多爬虫。修改下supervisord.conf.

	[program:cook]
	command=scrapy crawl cook
	directory=/home/cxy/lemon_spiders/cook
	user=cxy
然后用supervisorctl或web控制台连接到服务器。就可以一键启动任务了。
   
   ![404](https://github.com/aquairus/lemon_spiders/blob/master/doc/supervisord.png)

##Note

* 语料的抓取一般有去除html标签，但是保留'br' 'p'标签的要求。一开始我直接用re模块，把常用的标签都过滤掉。遇到新的标签再修改规则。后来发现[blench](http://bleach.readthedocs.org/en/latest/) 这个库具有白名单的功能。
* 从服务服务器上取数据的时候记得压缩，速度会快很多

##反省
conf不应该和代码混到一起，得改

#目录索引
下面是各目录的内容

目录 | 简介 | 
------------ | ------------- |
101 | 一开始没用框架自己写的爬虫 | 
ar| 抓取阿拉伯语新闻的爬虫| 
conf| 公钥 supervisor配置 初始化安装脚本 | 
cook| 抓cookbooks.com的爬虫  | 
douban| 抓豆瓣的爬虫 
kr| 抓韩语小说的爬虫 | 
nv| Content Cell  | 
selenium| 用了selenium  | 
tool| 数据库导出脚本 | 
yh| 抓yahoo问答的爬虫  | 
uy| 抓维吾尔新闻的爬虫| 
xm| 抓喜马拉雅电台的爬虫 | 

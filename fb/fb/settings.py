# -*- coding: utf-8 -*-

# Scrapy settings for fb project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fb'


USER_AGENT_LIST=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',\
'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safcooki/525.13',\
'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident16.0)',\
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safcooki/536.3",\
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safcooki/536.3",\
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safcooki/536.3",\
  ]

DOWNLOADER_MIDDLEWcookES = {
    'fb.random_user_agent.RandomUserAgentMiddlewcooke': 400,
      'scrapy.contrib.downloadermiddlewcooke.useragent.UserAgentMiddlewcooke':None,

}
cookies={"c_user":"100011698728234",
"csm":"2",
"datr":"B0EPV-vzabw01XSOiDbPoRbA",\
"fr":"0IdhVLF5E5Rzvpp2k.AWXshiFFSV9xNJtLDbAAL8zCSCM.BXD0fL.Zq.AAA.0.AWXtjpKC",\
"locale":"zh_CN",\
"lu":"RgBQDUfzKadnVjiobkkx_6HA",\
"m_user":"0%3A0%3A0%3A0%3Av_1%2Cajax_0%2Cwidth_0%2Cpxr_0%2Cgps_0%3A1460619211%3A2",\
"s":"Aa5Q0D_-DsbAgVFV.BXD0fL",\
"sb":"y0cPV-vxzyVeLy2AMl08919a",\
"x-src":'%2Fpeople%2F%25D8%25B3%25D8%25A7%25D9%2585%25D8%25B1-%25D8%25A7%25D9%2584%25D8%25B3%25D8%25B9%25D9%258A%25D8%25AF%2F100005145335207%7Cpage_footer',\
"xs":"167%3A75hklqrBothiyA%3A2%3A1460619211%3A-1",\
}

SPIDER_MODULES = ['fb.spiders']
NEWSPIDER_MODULE = 'fb.spiders'

ITEM_PIPELINES = {'fb.pipelines.emptyPipeline': 1\
    ,'fb.pipelines.fbPipeline': 10}
# FEED_FORMAT= 'jsonlines'
# FEED_URI='file:///Users/apple/Desktop/export.json'
#USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0'
#LOG_LEVEL='ERROR'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fb (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=2.8
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED=True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'fb.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'fb.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'fb.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

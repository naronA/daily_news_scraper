# -*- coding: utf-8 -*-

# Scrapy settings for news_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'news_crawler.pipelines.NewsCrawlerPipeline': 300,
}

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 7200
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
LOG_LEVEL = 'INFO'
FTP_ADDRESS = '172.16.27.200'
FTP_USER = 'crawlerpy'
FTP_PASS = 'crawlerpy'
FTP_NEWS_DIR = 'Crawler/YahooNews'
FTP_TOKEN_DIR = 'Crawler/TokenFiles'


FEED_URI = 'ftp://%(ftpuser)s:%(ftppass)s@%(ftpaddress)s/%(targetdir)s/%(category)s/%(category)s_%(starttime)s.%(format)s'

EXTENSIONS_BASE = {
    'scrapy.extensions.corestats.CoreStats': 0,
    'scrapy.extensions.telnet.TelnetConsole': 0,
    'scrapy.extensions.memusage.MemoryUsage': 0,
    'scrapy.extensions.memdebug.MemoryDebugger': 0,
    'scrapy.extensions.closespider.CloseSpider': 0,
    'news_crawler.exporters.FeedExporter': 0,
    'scrapy.extensions.logstats.LogStats': 0,
    'scrapy.extensions.spiderstate.SpiderState': 0,
    'scrapy.extensions.throttle.AutoThrottle': 0,
}

FEED_FORMAT = 'csv'
TOKEN_FEED_FORMAT = 'token'
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_FIELDS = ['category', 'title', 'manuscript_len', 'manuscript']
FEED_STORAGES_BASE = {
    '': 'scrapy.extensions.feedexport.FileFeedStorage',
    'file': 'scrapy.extensions.feedexport.FileFeedStorage',
    'stdout': 'scrapy.extensions.feedexport.StdoutFeedStorage',
    's3': 'scrapy.extensions.feedexport.S3FeedStorage',
    'ftp': 'news_crawler.exporters.FTPFeedStorage',
}


###### ORIGINAL SETTING #####

MECAB_DICTIONARY = ' -d /usr/lib/mecab/dic/mecab-ipadic-neologd'
NEWS_MAJOR_ITEMS = None # Noneなら全ニュース
# NEWS_MAJOR_ITEMS = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT・科学', 'ライフ', '地域']

# NEWS_MAJOR_ITEMS = ['地域']


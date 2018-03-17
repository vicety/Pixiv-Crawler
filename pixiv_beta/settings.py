# -*- coding: utf-8 -*-

# Scrapy settings for pixiv_beta project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import codecs
import os
import time
import configparser
from .utils.PixivError import settings_assert

# 验证配置文件
settings_assert()

# 读取配置
prj_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
os.chdir(prj_dir)
cf = configparser.ConfigParser()
cf.read_file(codecs.open("settings.ini", 'r', 'utf-8-sig'))


# 配置
BOT_NAME = 'pixiv_beta'
LOG_LEVEL = 'WARNING'

SPIDER_MODULES = ['pixiv_beta.spiders']
NEWSPIDER_MODULE = 'pixiv_beta.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pixiv_beta (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.60
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'pixiv_beta.middlewares.PixivBetaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'pixiv_beta.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'pixiv_beta.middlewares.PersistentCookiesMiddleware': 701,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pixiv_beta.pipelines.PixivBetaPipeline': 300,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    'pixiv_beta.pipelines.PixivBetaImagePipeline': 1,
}
IMAGES_MIN_WIDTH = cf.getint('IMG', 'MIN_WIDTH')
IMAGES_MIN_HEIGHT = cf.getint('IMG', 'MIN_HEIGHT')
IMAGES_URLS_FIELD = "img_url"

IMAGES_STORE = os.path.expanduser(cf.get('IMG', 'STORE_PATH'))
if os.path.isfile(IMAGES_STORE):
    print("using the default path")
    now_time = str(int(time.time()))
    os.mkdir(prj_dir + os.sep + 'images_' + now_time)
    IMAGES_STORE = os.path.join(prj_dir, 'images_' + now_time)
elif not os.path.exists(IMAGES_STORE):
    os.makedirs(IMAGES_STORE)
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

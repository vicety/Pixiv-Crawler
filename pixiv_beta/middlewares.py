# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


from __future__ import absolute_import

import os
import os.path
import logging
import pickle

from scrapy.http.cookies import CookieJar

from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
from scrapy import signals
from .settings import prj_dir


class PixivBetaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
        #request.meta['proxy'] = "http://127.0.0.1:8118"
        pass


class PersistentCookiesMiddleware(CookiesMiddleware):
    def __init__(self, debug=False):
        super(PersistentCookiesMiddleware, self).__init__(debug)
        self.load()

    def process_response(self, request, response, spider):
        # TODO: optimize so that we don't do it on every response
        res = super(PersistentCookiesMiddleware, self).process_response(request, response, spider)
        self.save()
        return res

    def getPersistenceFile(self):
        return os.path.join(prj_dir, '.cookie')

    def save(self):
        logging.debug("Saving cookies to disk for reuse")
        with open(self.getPersistenceFile(), "wb+") as f:
            pickle.dump(self.jars, f)
            f.flush()

    def load(self):
        filename = self.getPersistenceFile()
        logging.debug("Trying to load cookies from file '{0}'".format(filename))
        if not os.path.exists(filename):
            logging.info("File '{0}' for cookie reload doesn't exist".format(filename))
            return
        if os.path.isfile(filename):
            logging.info("File '{0}' is not a regular file".format(filename))

            with open(filename, "rb") as f:
                self.jars = pickle.load(f)
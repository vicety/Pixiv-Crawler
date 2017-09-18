import scrapy
import re

def isMultipleImage(self, response):
    see_more = response.css('.works_display .read-more.js-click-trackable::attr(href)').extract_first("")
    pass

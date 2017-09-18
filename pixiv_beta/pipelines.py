# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import re

class PixivBetaPipeline(object):
    def process_item(self, item, spider):
        return item

class PixivBetaImagePipeline(ImagesPipeline):
    header_base = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'
    header = {
        'Origin': 'https://accounts.pixiv.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    def extract_pid(self, url):
        return re.match('.*/(\d+)_p0.*', url)
    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            self.header['Referer'] = self.header_base.format(self.extract_pid(image_url))
            yield scrapy.Request(image_url, headers=self.header)

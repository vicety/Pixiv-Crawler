# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import re
import os
from .settings import IMAGES_STORE


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
    # title = ""
    os.chdir(IMAGES_STORE)

    def extract_pid(self, url):
        return re.match('.*/(\d+)_p0.*', url).group(1)

    def get_media_requests(self, item, info):
        if not ('img_url' in dict(item).keys()):
            return
        for image_url in item['img_url']:
            self.header['Referer'] = self.header_base.format(self.extract_pid(image_url))
            yield scrapy.Request(image_url, headers=self.header)

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.images_result_field in item.fields:
            item[self.images_result_field] = [x for ok, x in results if ok]
        img_paths = [x['path'] for ok, x in results if ok]
        os.rename(IMAGES_STORE+os.sep+img_paths[0], IMAGES_STORE+os.sep+'full'+os.sep+item['title']+"_"+item['pid']+'.jpg')
        return item

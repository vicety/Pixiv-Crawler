# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
import scrapy
import re
import os
import shutil
from .settings import IMAGES_STORE

class PixivBetaPipeline(object):
    def process_item(self, item, spider):
        return item


class PixivBetaImagePipeline(FilesPipeline):
    header_base = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'
    header = {
        'Origin': 'https://accounts.pixiv.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
    }
    # title = ""

    def extract_pid(self, url):
        return re.match('.*/(\d+)_p0.*', url).group(1)

    def get_media_requests(self, item, info):
        if not ('img_url' in dict(item).keys()):
            return
        for image_url in item['img_url']:
            try:
                self.header['Referer'] = item['referer']
            except KeyError as err:
                self.header['Referer'] = self.header_base.format(self.extract_pid(image_url))
            yield scrapy.Request(image_url, headers=self.header)

    def item_completed(self, results, item, info):
        img_paths = [x['path'] for ok, x in results if ok]
        if len(img_paths) > 0:
            ext = os.path.splitext(img_paths[0])[1]
            new_file_path = IMAGES_STORE + os.sep + 'full' + os.sep + item['title'] + "_" + item['pid'] + ext
            file_name = new_file_path.split(os.sep)[-1]
            os.rename(IMAGES_STORE + os.sep + img_paths[0], new_file_path)
            if 'p' in item["pid"]:
                dir_name = item["title"].replace(" ", "_").replace(os.sep, "_")
                if not os.path.exists("{0}/full/{1}".format(IMAGES_STORE, dir_name)):
                    os.mkdir("{0}/full/{1}".format(IMAGES_STORE, dir_name))
                shutil.move("{0}/full/{1}".format(IMAGES_STORE, file_name),
                            "{0}/full/{1}/{2}".format(IMAGES_STORE, dir_name, file_name))

            # deprecated in version 1.2.2
            if ext == '.zip':
                self.zip2gif(new_file_path)
        return item

    def zip2gif(self, file):
        from zipfile import ZipFile
        import imageio
        with ZipFile(file) as zip:
            zip_folder = file.replace('.zip', '')
            zip.extractall(zip_folder)
            with imageio.get_writer(file.replace('.zip', '.gif'), mode='I') as writer:
                for f in os.listdir(zip_folder):
                    writer.append_data(imageio.imread(os.path.join(zip_folder, f)))
                    #TODO: GIF帧率未实现，目前使用默认帧率
        os.remove(file)
        shutil.rmtree(zip_folder, ignore_errors=True)

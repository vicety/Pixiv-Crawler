import scrapy
import re
# from scrapy.xlib.pydispatch import dispatcher
# from scrapy.exceptions import CloseSpider
from scrapy.signalmanager import SignalManager
from urllib import parse
from ..utils.PixivError import *
from ..items import ImageItem
from scrapy.http.cookies import CookieJar
import requests
import codecs
import configparser
import os
import json
from ..settings import prj_dir
import math
from scrapy import Spider
from scrapy import signals
from ..utils.imgData import ImgData
import pickle

cf = configparser.ConfigParser()
os.chdir(prj_dir)
cf.read_file(codecs.open("settings.ini", 'r', 'utf-8-sig'))

class pixivSpider(Spider):
    name = "pixivSpider"
    collection_set = set()
    init_colletion_set_size = 0
    data = []
    process = 0
    maxsize = 1e9  # for debug only
    signalManger = SignalManager()
    entry = cf.get('PRJ', 'TARGET')

    if entry == "COLLECTION" and os.path.exists("./.trace"):
        with open("./.trace", "rb") as f:
            collection_set = pickle.load(f)
    init_colletion_set_size = len(collection_set)

    def __init__(self):
        super().__init__()
        self.DAILY_ST = cf.getint('DAILY', 'FROM')
        self.DAILY_END = cf.getint('DAILY', 'TO')
        start_page = (self.DAILY_ST-1)//50+1
        end_page = math.ceil(self.DAILY_END/50)+1
        self.ENTRY_URLS = {
            'COLLECTION': 'https://www.pixiv.net/bookmark.php',
            'ARTIST': ['https://www.pixiv.net/member_illust.php?id={0}'.format(pid) for pid in cf.get('ART', 'ID').split(' ')],
            'SEARCH': 'https://www.pixiv.net/search.php?s_mode=s_tag&word={0}'.format('%20'.join(cf.get('SRH', 'TAGS').split(" "))),
            'DAILY': ['https://www.pixiv.net/ranking.php?mode=daily&p={0}&format=json'.format(i) for i in range(start_page, end_page)],
        }
        self.ENTRY_FUNC = {
            'COLLECTION': self.collection,
            'ARTIST': self.artist,
            'SEARCH': self.search,
            'DAILY': self.daily
        }
        self.R18 = cf.getboolean('IMG', 'R18')
        self.MIN_WIDTH = cf.getint('IMG', 'MIN_WIDTH')
        self.MIN_HEIGHT = cf.getint('IMG', 'MIN_HEIGHT')
        self.MIN_FAV = cf.getint('IMG', 'MIN_FAV')
        self.entry = cf.get('PRJ', 'TARGET')
        self.account = cf.get('PRJ', 'ACCOUNT')
        self.password = cf.get('PRJ', 'PASSWORD')
        self.MULTI_IMAGE_ENABLED = cf.getboolean('IMG', 'MULTI_IMG_ENABLED')
        self.collection_num = -1
        self.all = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(pixivSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(cls.update_collection_set, signal=signals.item_scraped)
        return spider

    # allowed_domains = []
    start_urls = ['https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index']
    # agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'

    header = {
        'Origin': 'https://accounts.pixiv.net',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'User-Agent': agent,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'X-Requested-With': 'XMLHttpRequest',
    }
    cookie = 'p_ab_id=3; p_ab_id_2=4; bookmark_tag_type=count; bookmark_tag_order=desc; show_welcome_modal=1; ' \
             'module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%2' \
             '2name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_il' \
             'lusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7' \
             'D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22vis' \
             'ible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sense' \
             'i_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2' \
             'C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; device_token=480d576b6ad09b5a6' \
             '02e6f6fbb4b9593; __utmt=1; PHPSESSID=9deed4b733371c19ed8a86cf5b0c1c18; __utma=235335808.2088567130.' \
             '1501534936.1505413439.1505417847.41; __utmb=235335808.2.10.1505417847; __utmc=235335808; __utmz=235335808' \
             '.1505333595.35.9.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=235335808' \
             '.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=17759808=1^9=p_ab_id=3=1^10=p_ab_id_2=4=1^11' \
             '=lang=zh=1; login_bc=1; _ga=GA1.2.2088567130.1501534936; _gid=GA1.2.321153936.1505067374; _ga=GA1.3.2088567130.' \
             '1501534936; _gid=GA1.3.321153936.1505067374'

    # 入口
    def start_requests(self):
        if os.path.isfile(os.path.join(prj_dir, '.cookie')):
            #TODO: cookie不正确时跳转至login
            return self.center(None)
        else:
            return [scrapy.Request(self.start_urls[0], headers=self.header, callback=self.login)]

    def login(self, response):
        index_request = requests.get('http://www.pixiv.net', headers=self.header)
        index_cookie = index_request.cookies
        index_html = index_request.text
        pixiv_token = re.search(r'pixiv.context.token = (")(.*?)(")', index_html).group()
        start = pixiv_token.find('"')
        token = pixiv_token[start + 1:-1]
        # post_key = re.match('.*"pixivAccount.postKey":"(\w+?)"', response.text, re.S).group(1)
        print("please login")
        account = self.account if self.account else input("account >")
        password = self.password if self.password else input("password >")
        post_data = {
            "pixiv_id": account,
            "password": password,
            "captcha": "",
            "g_recaptcha_response": "",
            "post_key": token,
            "source": "pc",
            "ref": "wwwtop_accounts_index",
            "return_to": "http://www.pixiv.net/",
        }
        return [scrapy.FormRequest("https://accounts.pixiv.net/api/login?lang=zh",
                                   headers=self.header, formdata=post_data,
                                   callback=self.center, cookies=dict(index_cookie))]

    # 功能分支
    def center(self, response):
        if isinstance(self.ENTRY_URLS[self.entry], str):
            yield scrapy.Request(self.ENTRY_URLS[self.entry], headers=self.header, callback=self.ENTRY_FUNC[self.entry])
        else:
            print(len(self.ENTRY_URLS[self.entry]))
            for url in self.ENTRY_URLS[self.entry]:
                yield scrapy.Request(url, headers=self.header,
                                     callback=self.ENTRY_FUNC[self.entry])

    def collection(self, response):
        self.update_process(response, ".column-label .count-badge::text", 'Crawling collections...')
        image_items = response.css('._image-items.js-legacy-mark-unmark-list li.image-item')
        all_collection_urls = []

        for image_item in image_items:
            # 对于已经删除的图片 可能会包含在image_items中，但无法提取bookmark，在转为int时报错，程序到此终止
            # 在image_page会再检查一遍fav_num
            item_url = image_item.css('a.work._work::attr(href)').extract_first('')
            pid = item_url.split('illust_id=')[-1]
            if pid in self.collection_set:
                continue
            img_bookmark = image_item.css('ul li a.bookmark-count._ui-tooltip::text').extract_first('')
            if img_bookmark and int(img_bookmark) >= self.MIN_FAV:
                all_collection_urls.append(item_url)
        all_collection_urls = [parse.urljoin(response.url, url) for url in all_collection_urls]
        next_page_url = response.css('.column-order-menu .pager-container .next ._button::attr(href)').extract_first("")
        # ???
        if self.tryNextPage(next_page_url):
            next_page_url = parse.urljoin(response.url, next_page_url)
            yield scrapy.Request(next_page_url, headers=self.header, callback=self.collection)
        for url in all_collection_urls:
            yield scrapy.Request(url, headers=self.header, callback=self.image_page)

    def artist(self, response):
        self.update_process(response, "div._unit.manage-unit span.count-badge::text",
                            "Artist: {0}".format(response.css("._user-profile-card .profile a.user-name::text").extract_first('unknown')))
        all_works_url = response.css('ul._image-items li.image-item a.work._work::attr(href)').extract()
        all_works_url = [parse.urljoin(response.url, url) for url in all_works_url]
        next_page_url = response.css('.column-order-menu .pager-container .next ._button::attr(href)').extract_first("")
        if self.tryNextPage(next_page_url):
            next_page_url = parse.urljoin(response.url, next_page_url)
            yield scrapy.Request(next_page_url, headers=self.header, callback=self.artist)
        for url in all_works_url:
            yield scrapy.Request(url, headers=self.header, callback=self.image_page)

    def search(self, response):
        # for debug
        if self.process > self.maxsize:
            return
        js_text = response.css("div.layout-body div._unit input#js-mount-point-search-result-list::attr(data-items)").extract_first('Not Found')
        if js_text == "Not Found":
            print("json接口变动，烦请issue")
        js = json.loads(js_text)
        self.update_process(response, '._unit .column-header span.count-badge::text', 'Searching {0}'.format(cf.get('SRH', 'TAGS')))
        all_works_url = []
        for image_item in js:
            if image_item["bookmarkCount"] >= self.MIN_FAV:
                all_works_url.append(('https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(image_item["illustId"]),
                                      image_item['bookmarkCount']))
        next_page_url = response.css('.column-order-menu .pager-container .next ._button::attr(href)').extract_first("")
        if self.tryNextPage(next_page_url):
            next_page_url = parse.urljoin(response.url, next_page_url)
            yield scrapy.Request(next_page_url, headers=self.header, callback=self.search)
        for url, bookmarkCount in all_works_url:
            request = scrapy.Request(url, headers=self.header, callback=self.image_page)  # 就是这里改成提取数据
            request.meta['collection'] = bookmarkCount
            yield request

    def daily(self, response):
        self.all = self.DAILY_END - self.DAILY_ST + 1
        print("crawling process {0}/{1}".format(self.process, self.all))
        js = json.loads(response.text)
        for image_item in js['contents']:
            if not (image_item['rank'] < self.DAILY_ST or image_item['rank'] > self.DAILY_END):
                # self.process += 1
                yield scrapy.Request('https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}'.format(image_item['illust_id']),
                                     headers=self.header, callback=self.image_page)

    def image_page(self, response):
        if self.process > self.maxsize:
            return

        pid = re.match('.*id=(\d+)', response.request._url).group(1)
        img_data = self.extract_json(pid, response.body.decode('utf-8'))
        tags = [img_data["tags"]["tags"][i]['tag'] for i in range(len(img_data["tags"]["tags"]))]
        img_title = img_data["illustTitle"]
        img_title = img_title.replace(os.sep, '_').replace('/', '_')
        img_width, img_height = img_data["width"], img_data["height"]
        view = img_data["viewCount"]
        praise = img_data["likeCount"]
        r18 = True if tags[0] == 'R-18' else False

        if praise < self.MIN_FAV:
            return
        if (img_width < self.MIN_WIDTH or img_height < self.MIN_HEIGHT) or (self.R18 ^ r18):
            return
        if self.entry == "COLLECTION" and pid in self.collection_set:
            return

        try:
            print("Crawling {0}".format(img_title))
        except Exception as e:
            print("log部分暂未处理日语编码问题 不影响下载")
            pass
        finally:
            pass

        if img_data["pageCount"] > 1 and self.MULTI_IMAGE_ENABLED:
            # 先不统计多张图片的信息了 没时间写
            self.data.append(
                ImgData(img_title, pid, r18, view, praise, response.meta.setdefault('collection', ''), img_height,
                        img_width))
            see_more = "https://www.pixiv.net/member_illust.php?mode=manga&illust_id={}".format(pid)
            yield scrapy.Request(see_more, callback=self.multiImgPage)
            return

        is_gif = img_data["illustType"] == 2
        if(is_gif):
            print("该文件为gif文件，由于p站页面更新，还没找到接口，如果找到还请发个issue")

        img_item = ImageItem()
        img_url = img_data["urls"]["original"]

        img_item['is_gif'] = is_gif
        img_item["img_url"] = [img_url]
        img_item['title'] = img_title
        img_item['pid'] = str(pid)
        img_item['referer'] = response.url
        self.data.append(ImgData(img_title, pid, r18, view, praise,
                                 response.meta.setdefault('collection', ''), img_height, img_width))
        yield img_item

    def multiImgPage(self, response):
        # 多张图片的分辨率筛选交给pipeline去做
        son_urls = response.css('.manga .item-container a.full-size-container._ui-tooltip::attr(href)').extract()
        son_urls = [parse.urljoin(response.url, url) for url in son_urls]
        for url in son_urls:
            yield scrapy.Request(url, callback=self.multiImgPageSingle)

    # 未添加title
    def multiImgPageSingle(self, response):
        img_title = response.css('head title::text').extract_first("")
        img_title = img_title.replace(os.sep, '_')
        img_title = img_title.replace('/', '_')
        img_url = response.css('body img::attr(src)').extract_first("")
        img_item = ImageItem()
        img_item['is_gif'] = False
        img_item["img_url"] = [img_url]
        img_item["title"] = img_title
        img_item['pid'] = re.match('.*/(\d+_p\d*).*', img_url).group(1)
        img_item['referer'] = response.url
        yield img_item

    # called at page that contains multiple images
    def update_process(self, response, restr, log):
        if self.collection_num == -1:
            print("login successfully")
            # print(log.encode('gbk').decode('gbk'))  # 由于控制台程序中会出编码问题，这里先取消log 不会
            self.collection_num = response.css(restr).extract_first('')[:-1]
            print("found {0} result(s)".format(self.collection_num))
            if not self.collection_num:
                raise UnmatchError("collection_num not matched")
            self.all = self.collection_num
        else:
            print("crawling process {0}/{1}".format(self.process, self.all))

    def tryNextPage(self, next_page_url):
        if next_page_url:
            return True
        else:
            print("reached the last page")
            return False

    def extract_json(self, pid, text):
        query_text = pid + ": "
        start = text.find(query_text) + len(query_text)
        cnt = 0
        text = text[start:]
        for index, i in enumerate(text):
            if i == '{':
                cnt += 1
            elif i == '}':
                cnt -= 1
            if cnt == 0:
                text = text[:index + 1]
                return json.loads(text)

    @classmethod
    def update_collection_set(cls, item, response ,spider):
        # if cls.entry == "COLLECTION":
        cls.collection_set.add(item["pid"].split('_')[0])
        cls.process = len(cls.collection_set) - cls.init_colletion_set_size
        # for debug only
        if cls.process > cls.maxsize:
            if cls.entry == "COLLECTION":
                with open("./.trace", "wb") as f:
                    pickle.dump(cls.collection_set, f)

            # store .json file
            f = open("data_{0}.json".format('_'.join(cf.get('SRH', 'TAGS').split(" "))), 'w')
            data = [item.__dict__() for item in cls.data]
            json.dump(data, f)

            print("Crawling complete, got {0} data".format(len(cls.data)))
            f.close()
            os.abort()
            # raise CloseSpider
            # cls.signalManger.send_catch_log(signal=signals.spider_closed)

    def spider_closed(self, spider):
        # store .trace file
        if self.entry == "COLLECTION":
            with open("./.trace", "wb") as f:
                pickle.dump(self.collection_set, f)

        # store .json file
        f = open("data_{0}.json".format('_'.join(cf.get('SRH', 'TAGS').split(" "))), 'w')
        data = [item.__dict__() for item in self.data]
        json.dump(data, f)

        print("Crawling complete, got {0} data".format(len(self.data)))
        f.close()




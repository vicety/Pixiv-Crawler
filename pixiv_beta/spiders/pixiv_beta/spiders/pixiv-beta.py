import scrapy
import re
from urllib import parse
from pixiv_beta.utils.PixivError import *
from pixiv_beta.items import ImageItem
from scrapy.http.cookies import CookieJar
import requests

class pixivSpider(scrapy.Spider):

    process = 0
    all = 0
    name = "pixivSpider"
    # allowed_domains = []
    start_urls = ['https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index']
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    header_ori = {
        "Host": "accounts.pixiv.net",
        "Origin": "https://accounts.pixiv.net",
        "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
        "User-Agent": agent,
        "Connection": "keep-alive",
        # "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip, deflate, br",
        # "X-Requested-With": "XMLHttpRequest",
        "Cookie": "p_ab_id=3; p_ab_id_2=4; bookmark_tag_type=count; bookmark_tag_order=desc; show_welcome_modal=1; device_token=480d576b6ad09b5a602e6f6fbb4b9593; module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; PHPSESSID=3219b2a504870744423b7185cba55b26; login_bc=1; __utmt=1; __utma=235335808.2088567130.1501534936.1505314070.1505321297.32; __utmb=235335808.3.10.1505321297; __utmc=235335808; __utmz=235335808.1505295003.30.7.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=27609595=1^9=p_ab_id=3=1^10=p_ab_id_2=4=1^11=lang=zh=1; _ga=GA1.2.2088567130.1501534936; _gid=GA1.2.321153936.1505067374; _gat=1; _ga=GA1.3.2088567130.1501534936; _gid=GA1.3.321153936.1505067374; _gat_UA-76252338-4=1",
        # "Content-Length": "185",
        # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    header = {
        'Origin': 'https://accounts.pixiv.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'X-Requested-With': 'XMLHttpRequest',
    }
    cookie = 'p_ab_id=3; p_ab_id_2=4; bookmark_tag_type=count; bookmark_tag_order=desc; show_welcome_modal=1; module_orders_mypage=%5B%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; device_token=480d576b6ad09b5a602e6f6fbb4b9593; __utmt=1; PHPSESSID=9deed4b733371c19ed8a86cf5b0c1c18; __utma=235335808.2088567130.1501534936.1505413439.1505417847.41; __utmb=235335808.2.10.1505417847; __utmc=235335808; __utmz=235335808.1505333595.35.9.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=17759808=1^9=p_ab_id=3=1^10=p_ab_id_2=4=1^11=lang=zh=1; login_bc=1; _ga=GA1.2.2088567130.1501534936; _gid=GA1.2.321153936.1505067374; _ga=GA1.3.2088567130.1501534936; _gid=GA1.3.321153936.1505067374'

    def start_requests(self):
        self.cookie_jar = CookieJar()
        return [scrapy.Request(self.start_urls[0], headers=self.header, callback=self.login )]

    def login(self, response):
        index_request = requests.get('http://www.pixiv.net', headers=self.header)
        index_cookie = index_request.cookies
        index_html = index_request.text
        pixiv_token = re.search(r'pixiv.context.token = (")(.*?)(")', index_html).group()
        start = pixiv_token.find('"')
        token = pixiv_token[start + 1:-1]
        # post_key = re.match('.*"pixivAccount.postKey":"(\w+?)"', response.text, re.S).group(1)
        print("must login before using the function")
        account = input("account >")
        password = input("password >")
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
        return [scrapy.FormRequest("https://accounts.pixiv.net/api/login?lang=zh", headers=self.header, formdata=post_data, callback=self.center, cookies=dict(index_cookie))]

    def center(self, response):
        cmd = {"get_bookmark": self.collection}
        msg = "get_bookmark"
        self.process = 0
        yield scrapy.Request('https://www.pixiv.net/bookmark.php', headers=self.header, callback=cmd[msg])

    def collection(self, response):
        collection_num = -1
        if collection_num == -1:
            collection_num = response.css(".column-label .count-badge::text").extract_first('')[:-1]
            if not collection_num:
                raise UnmatchError("collection_num not matched")
            self.all = collection_num
        else:
            print("crawling process {0}/{1}".format(self.process, self.all))
        all_collection_urls = response.css('._image-items.js-legacy-mark-unmark-list li.image-item a.work._work::attr(href)').extract()
        all_collection_urls = [parse.urljoin(response.url, url) for url in all_collection_urls]
        next_page_url = response.css('.column-order-menu .pager-container .next ._button::attr(href)').extract_first("")
        if next_page_url:
            next_page_url = parse.urljoin(response.url, next_page_url)
            yield  scrapy.Request(next_page_url, headers=self.header, callback=self.collection)
        else:
            print("reached the last page")
        for url in all_collection_urls:
            yield scrapy.Request(url, headers=self.header, callback=self.image_page)

    def image_page(self, response):
        see_more = response.css('.works_display .read-more.js-click-trackable::attr(href)').extract_first("")
        if see_more:
            see_more = parse.urljoin(response.url, see_more)
            yield scrapy.Request(see_more, callback=self.multiImgPage)
            self.process += 1
            return
        img_item = ImageItem()
        img_url = response.css('div._illust_modal.ui-modal-close-box div.wrapper img.original-image::attr(data-src)').extract_first('')
        if not img_url:
            raise UnmatchError("image unmatched or not enough authority to visit the page when crawling {0}".format(response.url))
        img_item["img_url"] = [img_url]

        yield img_item

    def multiImgPage(self, response):
        son_urls = response.css('.manga .item-container a.full-size-container._ui-tooltip::attr(href)').extract()
        son_urls = [parse.urljoin(response.url, url) for url in son_urls]
        for url in son_urls:
            yield scrapy.Request(url, callback=self.multiImgPageSingle)


    def multiImgPageSingle(self, response):
        img_url = response.css('body img::attr(src)').extract_first("")
        img_item = ImageItem()
        img_item["img_url"] = [img_url]
        yield img_item


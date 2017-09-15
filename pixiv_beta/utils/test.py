# -*- coding:utf-8 -*-

import os
import re
import requests
import threading
from lxml import etree

index_url = 'http://www.pixiv.net'
login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
user_list = 'http://www.pixiv.net/bookmark.php?type=user'
member_illust = 'http://www.pixiv.net/member_illust.php?type=all'

header = {
    'Origin': 'https://accounts.pixiv.net',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    'X-Requested-With': 'XMLHttpRequest',
}

threads = []


class Pixiv_Login:
    def __init__(self, id, password):
        self.pixiv_id = id
        self.password = password
        self.header = header
        self.login_data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'captcha': '',
            'g_recaptcha_response': '',
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': 'http://www.pixiv.net/',
        }

    def get_cookie(self):
        index_request = requests.get(index_url, headers=self.header)
        index_cookie = index_request.cookies
        index_html = index_request.text
        d = dict(index_cookie)
        pixiv_token = re.search(r'pixiv.context.token = (")(.*?)(")', index_html).group()
        start = pixiv_token.find('"')
        token = pixiv_token[start + 1:-1]

        self.login_data["post_key"] = token
        login = requests.post(login_url, headers=self.header, cookies=index_cookie, data=self.login_data)
        return login.cookies

        # return login_cookies


class Pixiv_Scrapy:
    def __init__(self, cookies):
        self.login_cookies = cookies
        self.header = header

    def start(self):
        pass

    def get_users(self):
        user_list_html = requests.get(user_list, cookies=self.login_cookies)
        users = etree.HTML(user_list_html.text).xpath('//*[@id="search-result"]/div/ul/li/div[2]/a')

        # //*[@id="search-result"]/div/ul/li[1]/div[2]/a
        for user in users:
            # print(input.get('value'))
            user_id = user.get('data-user_id')
            user_name = user.get('data-user_name')
            os.makedirs('./' + user_name)
            self.get_by_userid(user_id, user_name)

    def get_by_userid(self, user_id, folderName):
        this_illust = member_illust + "&id=" + user_id

        image_path = '//*[@id="wrapper"]/div[1]/div[1]/div/div[4]/ul/li/a[1]'
        pages_path = '//*[@id="wrapper"]/div[1]/div[1]/div/ul[1]/div/ul/li/a'

        first_pages = etree.HTML(requests.get(this_illust, cookies=self.login_cookies, headers=self.header).text)
        pages = first_pages.xpath(pages_path)

        all_links = [this_illust, ]
        for page_index in pages:
            all_links.append(this_illust + "&p=" + page_index.text)

        for link in all_links:
            print(link)
            image_hrefs = etree.HTML(requests.get(link, cookies=self.login_cookies, headers=self.header).text).xpath(
                image_path)
            for href in image_hrefs:
                illust_link = index_url + href.get('href')
                print(illust_link)
                html_content = requests.get(illust_link, cookies=self.login_cookies, headers=self.header).text

                try:
                    a = etree.HTML(html_content).xpath('//*[@id="wrapper"]/div[1]/div[1]/div/div[6]/a/@href')
                    alt = etree.HTML(html_content).xpath('//*[@id="wrapper"]/div[1]/div[1]/div/div[6]/a/div/img/@alt')
                    alt = alt[0]
                    folderPath = folderName + "/" + alt
                    os.makedirs(folderPath)
                    print(folderName)
                    imgs = etree.HTML(requests.get(index_url + "/" + a[0], cookies=self.login_cookies,
                                                   headers=self.header).text).xpath(
                        '//*[@id="main"]/section/div/a/@href')
                    print("get a imges list")
                    for img_href in imgs:
                        img = etree.HTML(requests.get(index_url + img_href, cookies=self.login_cookies,
                                                      headers=self.header).text).xpath('/html/body/img')
                        img = img[0]
                        src = img.get("src")
                        t = threading.Thread(target=self.download,
                                             args=(src, index_url + img_href, folderPath + "/" + src.split('/')[-1]))
                        t.start()
                except:
                    try:
                        # //*[@id="wrapper"]/div[2]/div/img
                        img = etree.HTML(html_content).xpath('//*[@id="wrapper"]/div[2]/div/img')
                        img = img[0]
                        print("get only one image")
                        src = img.get('data-src')
                        t = threading.Thread(target=self.download, args=(
                        src, illust_link, folderName + "/" + img.get('alt') + "." + src.split(".")[-1]))
                        t.start()
                    except:
                        print("not a picture")

    def download(self, src, referer, fileName):
        print('start-' + src)
        href_header = header
        href_header["Referer"] = referer
        r = requests.get(src, headers=href_header, stream=True)
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                f.flush()
            f.close()
        print(src + '-saved')


if __name__ == '__main__':
    Pixiv_Scrapy(Pixiv_Login('vicety', 'PA19981031').get_cookie()).get_users()
import scrapy
from amazonscraping.items import AmazonscrapingItem
from scrapy.conf import settings
import hashlib
from selenium import webdriver
import os
import urlparse
import re


class AmazonSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ['amazon.com']
    start_url = 'https://www.amazon.com'
    # start_url = 'https://www.amazon.com/Vancouver-Historical-Society-Newsletter/dp/B000E5N2II/ref=lp_16416041_1_12?s=magazines&ie=UTF8&qid=1539271349&sr=1-12'

    HEADER = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/67.0.3396.99 Safari/537.36"}

    def __init__(self, *args, **kwargs):
        self.screenshot = kwargs.get('screenshot', None)
        if self.screenshot in (True, 'True', 'true'):
            self.screenshot = True
        else:
            self.screenshot = False

        super(AmazonSpider, self).__init__(
            site_name=self.allowed_domains[0],
            *args, **kwargs)

        settings.overrides['DEFAULT_REQUEST_HEADERS'] = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }

    def start_requests(self):
        yield scrapy.Request(self.start_url,
                             callback=self.parse_links, headers=self.HEADER)

    # def start_requests(self):
    #     yield scrapy.Request(self.start_url,
    #                          callback=self.parse_product, headers=self.HEADER)

    def parse_links(self, response):
        search_alias_list = response.xpath('//select[@id="searchDropdownBox"]/option/@value').extract()
        for alias in search_alias_list:
            url = 'https://www.amazon.com/s/ref=nb_sb_noss?url={}&field-keywords='.format(alias)
            yield scrapy.Request(url, callback=self.parse_categories,
                                 headers=self.HEADER, dont_filter=True)

    def parse_categories(self, response):
        categories = response.xpath('//ul[contains(@class, "a-unordered-list")]'
                                    '//li//a[contains(@class, "a-link-normal")]/@href').extract()
        for category in categories:
            link = urlparse.urljoin(response.url, category)
            yield scrapy.Request(link, callback=self.parse_sub_categories,
                                 headers=self.HEADER, dont_filter=True)

    def parse_sub_categories(self, response):
        sub_categories = response.xpath('//ul[contains(@class, "a-unordered-list")]'
                                        '//li//a[contains(@class, "a-link-normal")]/@href').extract()
        for sub_category in sub_categories:
            link = urlparse.urljoin(response.url, sub_category)
            yield scrapy.Request(link, callback=self.parse_last_categories,
                                 headers=self.HEADER, dont_filter=True)

    def parse_last_categories(self, response):
        last_categories = response.xpath('//ul[contains(@class, "a-unordered-list")]'
                                         '//li//a[contains(@class, "a-link-normal")]/@href').extract()
        for last_category in last_categories:
            link = urlparse.urljoin(response.url, last_category)
            yield scrapy.Request(link, callback=self.parse_product_links,
                                 headers=self.HEADER, dont_filter=True)

    def parse_product_links(self, response):
        links = response.xpath('//div[@id="mainResults"]/ul/li'
                               '//a[contains(@class, "a-link-normal")]/@href').extract()
        for link in links:
            link = urlparse.urljoin(response.url, link)
            yield scrapy.Request(url=link, callback=self.parse_product,
                                 headers=self.HEADER, dont_filter=True)

    def parse_product(self, response):
        item = AmazonscrapingItem()

        item['url'] = response.url

        name = response.xpath('//span[@id="productTitle"]/text()').extract()
        if not name:
            name = response.xpath('//*[@id="title"]/text()').extract()
        if not name:
            name = response.xpath('//div[@id="product-title"]/h1/text()').extract()
        if not name:
            name = response.xpath('//*[@id="title"]/span/text()').extract()

        if name:
            item['title'] = name[0].strip()

        brand = response.xpath('//div/@data-brand').extract()
        if not brand:
            brand = re.findall('"brand":"(.*?)",', response.body, re.DOTALL)

        if brand:
            item['brand'] = brand[0].strip()

        price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
        if not price:
            price = response.xpath('//span[contains(@class, "a-color-price")]/text()').extract()
        if price:
            if '-' in price[0]:
                item['price'] = price[0].split('-')[0].strip()
            else:
                item['price'] = price[0].strip()
        else:
            item['price'] = None

        price_discount = response.xpath('//span[contains(@class, "snsSavings")]/text()').re('\d+.\d+')
        if price_discount:
            price_discount = price_discount[0]
            item['price_discount'] = price_discount
        else:
            item['price_discount'] = None

        if self.screenshot:
            driver_path = '/usr/sbin/chromedriver'
            if not os.path.exists(driver_path):
                driver_path = '/usr/local/bin/chromedriver'
            driver = webdriver.Chrome(driver_path)
            driver.get(response.url)
            url_hash = hashlib.md5(item['url'].encode("utf8")).hexdigest()
            filename = "{}.png".format(url_hash)
            driver.save_screenshot(filename)
            driver.quit()
            item['screenshot_filename'] = filename

        yield item

import scrapy
from amazonscraping.items import AmazonscrapingItem
from scrapy.conf import settings


class AmazonSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ['amazon.com']
    start_url = 'https://www.amazon.com/gp/product/B00FMWWN6U/ref=s9_acsd_top_hd_bw_bBDf7D_cr_x__w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-5&pf_rd_r=4HH62GZAN2NBGY26PP81&pf_rd_r=4HH62GZAN2NBGY26PP81&pf_rd_t=101&pf_rd_p=f58ea2ad-c233-5131-9794-50b9ee3a9e5e&pf_rd_p=f58ea2ad-c233-5131-9794-50b9ee3a9e5e&pf_rd_i=165796011'

    HEADER = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/67.0.3396.99 Safari/537.36"}

    def __init__(self, *args, **kwargs):
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
                             callback=self.parse_product, headers=self.HEADER)

    def parse_product(self, response):
        item = AmazonscrapingItem()

        item['url'] = response.url

        name = response.xpath('//span[@id="productTitle"]/text()').extract()
        if not name:
            name = response.xpath('//*[@id="title"]/text()').extract()

        if name:
            item['title'] = name[0].strip()

        brand = response.xpath('//div/@data-brand').extract()

        if brand:
            item['brand'] = brand[0].strip()

        price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
        if not price:
            price = response.xpath('//span[@class="a-color-price"]/text()').extract()
        if price:
            if '-' in price[0]:
                item['price'] = price[0].split('-')[0].strip()
            else:
                item['price'] = price[0]

        price_discount = response.xpath('//span[contains(@class, "snsSavings")]/text()').re('\d+.\d+')[0]
        item['price_discount'] = price_discount

        return item

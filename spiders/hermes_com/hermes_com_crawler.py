from typing import Iterable, Optional, List
import logging
from scrapy.spiders import XMLFeedSpider
import scrapy
from scrapy.utils.response import open_in_browser as view

from spiders.hermes_com.hermes_com_parser import HermesComParser

logger = logging.getLogger(__name__)


class HermesComCrawler(XMLFeedSpider):
    name = "us_dolcegabbana_com"
    start_urls = [
        'https://www.hermes.com/sitemap.xml'
    ]
    itertag = 'loc'
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 3
    }

    def __init__(self):
        super().__init__()
        self.parser = HermesComParser

    @classmethod
    def headers(cls) -> dict:
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'upgrade-insecure-requests': '1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'te': 'trailers'}

    def parse_nodes(self, response, node) -> Iterable:
        category_urls = []
        for item in node:
            url = item.xpath('text()').get()
            if not 'category' in url:
                continue
            splitted_url = url.split('category', 1)
            category = splitted_url[1].strip('/').replace('-', ' ').replace('/', ', ')
            category_urls.append({'url': url, 'category': category})
        yield scrapy.Request(url='https://www.hermes.com/us/en/',
                             callback=self.serch_products,
                             #headers=self.headers(),
                             cb_kwargs={'category_urls': category_urls})

    def serch_products(self, response, category_urls: List):
        for item_dict in category_urls:
            yield scrapy.Request(url=item_dict.get('url'),
                                 callback=self.parse_products,
                                 headers=self.headers(),
                                 cb_kwargs={'category': item_dict.get('category')})

    def parse_products(self, response, category):
        for product in self.parser.parse_products(response, category):
            yield product

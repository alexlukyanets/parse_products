from typing import Iterable, Optional
import logging
import scrapy

from spiders.us_dolcegabbana_com.us_dolcegabbana_com_parser import UsDolcegabbanaComParser

logger = logging.getLogger(__name__)


class UsDolcegabbanaComCrawler(scrapy.Spider):
    name = "us_dolcegabbana_com"

    def __init__(self):
        super().__init__()
        self.parser = UsDolcegabbanaComParser

    @staticmethod
    def domain_url() -> str:
        return 'https://us.dolcegabbana.com/en/'

    @staticmethod
    def extract_category_text(a_tag) -> Optional[str]:
        category_text = a_tag.xpath('text()').get()
        if category_text:
            return category_text.strip()

    def start_requests(self)-> Iterable:
        yield scrapy.Request(
            url=self.domain_url(),
            callback=self.parse_categories
        )

    def parse_categories(self, response) -> Iterable:
        for a_tag in response.xpath('//a[contains(@class, "menu_category-link")]'):
            category_text = self.extract_category_text(a_tag)
            yield scrapy.Request(
                url=a_tag.xpath('@href').get(),
                callback=self.parse_subcategories, dont_filter=True,
                cb_kwargs={'category': category_text}
            )

    def parse_subcategories(self, response, category: str) -> Iterable:
        for url in response.xpath('//a[contains(text(), "View all")]/@href').getall():
            yield scrapy.Request(
                url=url,
                callback=self.parse_products,
                cb_kwargs={'category': category}
            )

    def parse_products(self, response, category: str) -> Iterable:
        for product in self.parser.parse_products(response, category):
            yield product

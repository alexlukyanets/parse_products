import logging
from typing import Optional

from scrapy import Selector
from scrapy.utils.response import open_in_browser as view

from items import ProductItem

logger = logging.getLogger(__name__)

class UsDolcegabbanaComParser:
    @classmethod
    def extract_product_price(cls, div_tag: Selector) -> Optional[str]:
        price_str = cls.find_by_tag_pattern(div_tag, 'div[contains(@class, "price")]/text()')
        if not price_str:
            return
        return price_str.strip()

    @staticmethod
    def find_by_tag_pattern(div_tag, xpath_str) -> Optional[str]:
        for _ in range(20):
            if div_tag.xpath(f'{xpath_str}'):
                return div_tag.xpath(f'{xpath_str}').get()
            xpath_str = 'div/' + xpath_str

    @classmethod
    def parse_products(cls, response, category: str):
        div_tags = response.xpath('//div[contains(@class, "product_tile")][@id]')
        if not div_tags:
            logger.info(f'Unable to find required div tags for {response.url} link')
            return
        for div_tag in div_tags:
            product_item = ProductItem()
            product_item.url = cls.find_by_tag_pattern(div_tag, 'a/@href')
            if product_item.url:
                product_item.url = response.urljoin(product_item.url)
            if not product_item.url:
                logger.info('Unable to find product url')
                continue
            product_item.name = cls.find_by_tag_pattern(div_tag, 'a/@title')
            if not product_item.name:
                logger.info('Unable to find product name')
                continue
            product_item.price = cls.extract_product_price(div_tag)
            if not product_item.price:
                logger.info('Unable to find product price')
            product_item.image_url = cls.find_by_tag_pattern(div_tag, 'a/picture/img/@data-src')
            product_item.category = category
            yield product_item

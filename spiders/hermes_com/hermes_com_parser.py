import logging
from typing import Optional

from scrapy import Selector
from scrapy.utils.response import open_in_browser as view

from items import ProductItem

logger = logging.getLogger(__name__)


class HermesComParser:
    @classmethod
    def extract_product_price(cls, div_tag: Selector) -> Optional[str]:
        price_str = div_tag.xpath('a/div/div/h-price/span/text()').get()
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
        div_tags = response.xpath('//div[@class="product-item"]')
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
            product_item.name = div_tag.xpath('a/div/span[contains(@class, "item-name")]/text()').get()
            if not product_item.name:
                logger.info('Unable to find product name')
                continue
            product_item.name = product_item.name.strip()
            product_item.price = cls.extract_product_price(div_tag)
            if not product_item.price:
                logger.info('Unable to find product price')
            product_item.image_url = div_tag.xpath('a/div/h-image-resizer/picture/noscript/img/@src').get()
            if product_item.image_url:
                product_item.image_url = response.urljoin(product_item.image_url)
            product_item.category = category
            yield product_item

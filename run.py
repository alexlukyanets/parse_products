from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.us_dolcegabbana_com.us_dolcegabbana_com_crawler import UsDolcegabbanaComCrawler
from spiders.hermes_com.hermes_com_crawler import HermesComCrawler

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

runner.crawl(HermesComCrawler)

d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()

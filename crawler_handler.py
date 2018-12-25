from datetime import datetime
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import notifier_handler
from sales_monitor.spiders.next_ie import NextIeSpider

log = logging.getLogger()
log.setLevel(logging.INFO)


def handler(event, context):
    process = CrawlerProcess(get_project_settings())
    process.crawl(NextIeSpider)
    process.start()  # the script will block here until the crawling is finished
    print('Finish crawler', event['store_name'], datetime.now())
    notifier_handler.handler(event, context)


if __name__ == "__main__":
    event = {'store_name': 'next.ie', 'threshold': 1, 'hours': 12}
    handler(event, '')

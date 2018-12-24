import logging
from datetime import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import monitor_handler
from sales_monitor.spiders.next_ie import NextIeSpider

log = logging.getLogger()
log.setLevel(logging.INFO)


def main(event, context):
    process = CrawlerProcess(get_project_settings())
    process.crawl(NextIeSpider)
    process.start()  # the script will block here until the crawling is finished
    print('Finish crawler', event['store_name'], datetime.now())
    monitor_handler.main(event, context)


if __name__ == "__main__":
    event = {'store_name': 'next.ie', 'threshold': 1, 'hours': 12}
    main(event, '')

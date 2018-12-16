import calendar
import json
import pkgutil
import scrapy
from datetime import datetime


class BaseSpider(scrapy.Spider):

    def start_requests(self):
        products = json.loads(pkgutil.get_data('sales_monitor', 'resources/urls.json').decode())
        for name, urls in products.items():
            for url in urls:
                if self.name in url:
                    now = datetime.now()
                    epoch_time = calendar.timegm(now.timetuple())
                    item = {'epoch_time': epoch_time, 'product_name': name, 'retailer': self.name, 'created_at': now}
                    # yield scrapy.Request(url, meta={'item': item})
                    yield scrapy.Request(url, meta={'item': item, 'original_url': url})

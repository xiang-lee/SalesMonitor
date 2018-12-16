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
                    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    product_id = self.name + '-' + name + '-' + now # primary key
                    item = {'product_id': product_id, 'product_name': name, 'retailer': self.name, 'created_at': now}
                    # yield scrapy.Request(url, meta={'item': item})
                    yield scrapy.Request(url, meta={'item': item, 'original_url': url})

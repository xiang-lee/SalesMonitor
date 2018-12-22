from _decimal import Decimal

from .base_spider import BaseSpider


class NextIeSpider(BaseSpider):
    name = 'next.ie'

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.meta.get('original_url')
        item['title'] = response.css("div.Title > h1 ::text").extract_first().strip()

        # The price can be a range. e.g. €18.50 - €25
        price_string = response.css('div.Price > div > span ::text').extract_first(default=0).replace('€', '')
        price = price_string.split('-')[0].strip()
        item['price'] = Decimal(price)

        yield item

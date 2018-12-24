import calendar
from _operator import itemgetter
from datetime import datetime, timedelta

from jinja2 import Environment, PackageLoader

from sales_monitor import settings, email_utils
from sales_monitor.dynamodb_utils import DynamoDbUtils
from sales_monitor.utils import get_product_names, get_retailers_for_product

jinja_env = Environment(loader=PackageLoader('sales_monitor', 'templates'))

CHARSET = "UTF-8"


class ProductsChecker(object):

    def __init__(self, latest_products, previous_products, price_threshold=0):
        self.price_threshold = price_threshold
        self.latest_products = latest_products
        self.previous_products = previous_products

    def is_from_latest_crawl(self, product):
        """Checks whether the given product is from the most recent execution.
        """
        return product in self.latest_products

    def get_best_product(self):
        """Returns the item with the best overall price. self.price_threshold can be set to avoid
           considering minor price drops.
        """
        if self.previous_products and self.latest_products:
            best_so_far = min(self.previous_products, key=lambda x: x.get('price'))
            best_from_last = min(self.latest_products, key=lambda x: x.get('price'))
            if best_from_last.get('price') + self.price_threshold <= best_so_far.get('price'):
                return best_from_last
            else:
                return best_so_far


class ProductsFetcher(object):

    def __init__(self, product_name, hours):
        self.products = None
        self.dynamoDbUtils = DynamoDbUtils()
        self.product_name = product_name
        self.load_items_from_last_n_hours(hours, product_name)

    def load_items_from_last_n_hours(self, hours=24, product_name=None):
        """Load items from the last n hours, from the newest to the oldest.
        """
        since_time = datetime.now() - timedelta(hours=hours)
        since_epoch_time = calendar.timegm(since_time.timetuple())
        self.products = self.dynamoDbUtils.get_items_newer_than(settings.DYNAMODB_PRODUCT_TABLE_NAME, product_name,
                                                                since_epoch_time)

    def get_latest_product_from_retailer(self, retailer):
        """Returns the most recently extracted product from a given retailer.
        """
        sorted_products = sorted(self.products, key=itemgetter('epoch_time'), reverse=True)
        for products in sorted_products:
            if retailer in products.get('url'):
                return products
        return []

    def get_products(self):
        """Returns a tuple with (products from latest crawl, products from previous crawls)
        """
        latest_products = [
            self.get_latest_product_from_retailer(retailer)
            for retailer in get_retailers_for_product(self.product_name)
        ]
        previous_products = [
            product for product in self.products if product not in latest_products
        ]
        return latest_products, previous_products


def check_and_notify(threshold, hours):
    print('---start check_and_notify----', datetime.now())
    items = []
    for prod_name in get_product_names():
        fetcher = ProductsFetcher(prod_name, hours)
        checker = ProductsChecker(*fetcher.get_products(), threshold)
        best_product = checker.get_best_product()
        if checker.is_from_latest_crawl(best_product):
            items.append(best_product)
    if items:
        print('Sale!. Items on sale: ', items)
        email_utils.send_email_alert(items)
    else:
        print('not sale!')


def main(event, context):
    check_and_notify(event['threshold'], event['hours'])


if __name__ == '__main__':
    event = {'threshold': 1, 'hours': 1}
    main(event, '')

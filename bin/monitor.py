import argparse
import os
from datetime import datetime, timedelta

from jinja2 import Environment, PackageLoader
from scrapinghub import ScrapinghubClient

from sales_monitor import settings
from sales_monitor.email_utils import send_email_alert
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
        best_so_far = min(self.previous_products, key=lambda x: x.get('price'))
        best_from_last = min(self.latest_products, key=lambda x: x.get('price'))
        if best_from_last.get('price') + self.price_threshold <= best_so_far.get('price'):
            return best_from_last
        else:
            return best_so_far


class ProductsFetcher(object):

    def __init__(self, product_name, apikey, project_id, hours):
        self.product_name = product_name
        project = ScrapinghubClient(apikey).get_project(project_id)
        self.item_store = project.collections.get_store(product_name)
        self.load_items_from_last_n_hours(hours)

    def load_items_from_last_n_hours(self, n=24):
        """Load items from the last n hours, from the newest to the oldest.
        """
        since_time = int((datetime.now() - timedelta(hours=n)).timestamp() * 1000)
        self.products = [item.get('value') for item in self.fetch_products_newer_than(since_time)]

    def fetch_products_newer_than(self, since_time):
        return list(self.item_store.iter(startts=since_time))

    def get_latest_product_from_retailer(self, retailer):
        """Returns the most recently extracted product from a given retailer.
        """
        for products in self.products:
            if retailer in products.get('url'):
                return products

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

        print('latest_products = ', latest_products)
        print('previous_products = ', previous_products)

        return latest_products, previous_products


def main(args):
    items = []
    for prod_name in get_product_names():
        fetcher = ProductsFetcher(prod_name, args.apikey, args.project, args.days * 24)
        checker = ProductsChecker(*fetcher.get_products(), args.threshold)
        best_product = checker.get_best_product()
        if checker.is_from_latest_crawl(best_product):
            items.append(best_product)
    if items:
        send_email_alert(items)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apikey', default=settings.SHUB_KEY or os.getenv('SHUB_KEY'),
                        help='API key to use for scrapinghub (fallbacks to SHUB_KEY variable)')
    parser.add_argument('--days', type=int, default=1,
                        help='How many days back to compare with the last price')
    parser.add_argument('--threshold', type=float, default=0,
                        help='A margin to avoid raising alerts with minor price drops')
    parser.add_argument('--project', type=int, default=settings.SHUB_PROJ_ID,
                        help='Project ID to get info from')

    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())

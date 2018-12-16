# -*- coding: utf-8 -*-

from sales_monitor import settings
from sales_monitor.dynamodb_utils import DynamoDbUtils


class CollectionStoragePipeline(object):

    def __init__(self):
        self.dynamoDbUtils = DynamoDbUtils()

    def process_item(self, item, spider):
        self.dynamoDbUtils.add_items(settings.DYNAMODB_PRODUCT_TABLE_NAME, item.items())
        return item

# -*- coding: utf-8 -*-

BOT_NAME = 'sales_monitor'
SPIDER_MODULES = ['sales_monitor.spiders']
NEWSPIDER_MODULE = 'sales_monitor.spiders'

ROBOTSTXT_OBEY = True

AWS_ACCESS_KEY = '<key>'
AWS_SECRET_KEY = '<secret>'
REGION_NAME = 'eu-west-1'
DYNAMODB_PRODUCT_TABLE_NAME = 'SalesMonitorProduct'

# settings for email
EMAIL_ALERT_FROM = 'xiangli.dev@gmail.com'
EMAIL_ALERT_TO = ['xiangireland@gmail.com']

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sales_monitor.pipelines.CollectionStoragePipeline': 400,
}

AUTOTHROTTLE_ENABLED = True
# HTTPCACHE_ENABLED = True

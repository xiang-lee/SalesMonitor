# -*- coding: utf-8 -*-
import os

BOT_NAME = 'sales_monitor'
SPIDER_MODULES = ['sales_monitor.spiders']
NEWSPIDER_MODULE = 'sales_monitor.spiders'

ROBOTSTXT_OBEY = True

SHUB_KEY = os.getenv('SH_APIKEY', '')
# if you want to run it locally, replace '999999' by your Scrapy Cloud project ID below
SHUB_PROJ_ID = os.getenv('SHUB_JOBKEY', '').split('/')[0]


# settings for email
EMAIL_ALERT_FROM = 'xiangli.dev@gmail.com'
EMAIL_ALERT_FROM_PASSWORD = '<YOUR_PASSWORD>'
EMAIL_ALERT_TO = ['xiangireland@gmail.com']

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sales_monitor.pipelines.CollectionStoragePipeline': 400,
}

AUTOTHROTTLE_ENABLED = True
# HTTPCACHE_ENABLED = True

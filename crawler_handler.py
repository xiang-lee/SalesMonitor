import logging
from subprocess import Popen

log = logging.getLogger()
log.setLevel(logging.INFO)


def main(event, context):
    store_name = event['store_name']
    log.info('starting crawl: ' + store_name)
    print('print starting crawl: ', store_name)
    process = Popen(['scrapy', 'crawl', event['store_name']])
    process.communicate()


if __name__ == "__main__":
    event = {'store_name': 'next.ie'}
    main(event, '')

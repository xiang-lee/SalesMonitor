import datetime

import boto3

from sales_monitor import settings


def default_encoder(value):
    if isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, datetime.time):
        return value.strftime('%H:%M:%S')
    else:
        return value


class DynamoDbUtils(object):
    def __init__(self, encoder=default_encoder):
        self.encoder = encoder
        self.db = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.DYNAMODB_PIPELINE_REGION_NAME,
        )

    def add_items(self, table_name, items):
        table = self.db.Table(table_name)
        return table.put_item(
            TableName=table_name,
            Item={k: self.encoder(v) for k, v in items},
        )

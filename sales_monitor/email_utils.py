import boto3
from botocore.exceptions import ClientError
from jinja2 import Environment, PackageLoader

from sales_monitor import settings

jinja_env = Environment(loader=PackageLoader('sales_monitor', 'templates'))
SUBJECT = 'Price drop alert'
CHARSET = "UTF-8"


def send_email_alert(items):
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
    )
    ses = session.client('ses', settings.REGION_NAME)
    html_body = jinja_env.get_template('email.html').render(items=items)
    email_subject = SUBJECT
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': settings.EMAIL_ALERT_TO
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': html_body,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': email_subject,
                },
            },
            Source=settings.EMAIL_ALERT_FROM
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent!"),
        print(response['MessageId'])

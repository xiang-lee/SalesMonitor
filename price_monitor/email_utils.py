import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys
from jinja2 import Environment, PackageLoader

from price_monitor import settings

jinja_env = Environment(loader=PackageLoader('price_monitor', 'templates'))
SUBJECT = 'Price drop alert'


def send_email_alert(items):
    print('sending email - xiang123')
    html_body = jinja_env.get_template('email.html').render(items=items)
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = settings.EMAIL_ALERT_FROM
    msg['To'] = ", ".join(settings.EMAIL_ALERT_TO)
    msg.preamble = 'preamble'
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.ehlo()
        # server.starttls()
        # server.login(settings.EMAIL_ALERT_FROM, settings.EMAIL_ALERT_FROM_PASSWORD)
        # server.sendmail(settings.EMAIL_ALERT_FROM, settings.EMAIL_ALERT_TO, msg.as_string())
        # server.quit()
        print('Email sent!')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Something went wrong...', e)
        print(exc_type, fname, exc_tb.tb_lineno)

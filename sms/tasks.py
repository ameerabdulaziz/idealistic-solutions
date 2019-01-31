from __future__ import absolute_import, unicode_literals
from celery import Celery,shared_task
from twilio.rest import Client

# app1 = Celery('sms')


@app1.task
def send_sms():
    pass

from __future__ import absolute_import, unicode_literals
from celery import Celery,shared_task
# For emails
import os
import smtplib
import os.path
from email.mime.text import MIMEText

app1 = Celery('accounts')
app2 = Celery('accounts')
app3 = Celery('accounts')

@app1.task
def test1(x, y):
    return x + y

@app2.task
def test2(x, y):
    return x * y

@app3.task
def email():
    print ("Sending")
    # Message
    msg = MIMEText("WARNING, FILE DOES NOT EXISTS, THAT MEANS UPDATES MAY DID NOT HAVE BEEN RUN")
    # Subject
    msg['Subject'] = "WARNING WARNING ON FIRE FIRE FIRE!"
    x = ['Eslam@idealisticsolutions.com']
    #put your host and port here
    s = smtplib.SMTP_SSL('smtp.gmail.com:465')
    s.login('datateam.ac@gmail.com','@ppliancesConnection')
    s.sendmail('datateam.ac@gmail.com',x, msg.as_string())
    s.quit()
    #print ("done")
    return ('Done')

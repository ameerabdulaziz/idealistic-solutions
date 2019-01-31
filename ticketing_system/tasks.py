from __future__ import absolute_import, unicode_literals
from celery import Celery,shared_task

# app1 = Celery('ticketing_system')
# app2 = Celery('ticketing_system')
#
# @app1.task
# def test1(x, y):
#     return x + y
#
# @app2.task
# def test2(x, y):
#     return x * y

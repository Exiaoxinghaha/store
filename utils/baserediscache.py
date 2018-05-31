# -*-coding:utf-8-*-
from django_redis import get_redis_connection

class BaseBrowse():
    def __init__(self):
        self.connect = get_redis_connection('default')
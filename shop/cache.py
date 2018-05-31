# -*-coding:utf-8-*-
from utils.baserediscache import BaseBrowse

# 用户浏览记录
class User_Browse_History_Cache(BaseBrowse):
    key = '{}_browse_history'
    def add_cache(self,key,gid):
        self.connect.lpush(self.key.format(key),gid)
    def show_cache(self,key):
        return self.connect.lrange(self.key.format(key),0,10)
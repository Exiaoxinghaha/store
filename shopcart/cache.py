# -*-coding:utf-8-*-
from utils.baserediscache import BaseBrowse

class User_Cart_Cache(BaseBrowse):
    key = '{}_cart'
    def cart_append_good_cache(self,sessionid,gid,buy_num):
        self.connect.hset(self.key.format(sessionid),gid,buy_num)
    def get_cart_len_cache(self,sessionid):
        return self.connect.hlen(self.key.format(sessionid))
    def getall_goods_cache(self,sessionid):
        return self.connect.hgetall(self.key.format(sessionid))
    def delete_goods_cache(self,sessionid,gid):
        self.connect.hdel(self.key.format(sessionid),gid)
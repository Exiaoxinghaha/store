# -*-coding:utf-8-*-
import random

def order_code(length=20):
    num_list = [str(i) for i in range(100)]
    code_list = random.sample(num_list,length)
    code = ''.join(code_list)
    return code

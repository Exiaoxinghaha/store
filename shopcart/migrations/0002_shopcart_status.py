# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-05 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '正常'), (1, '删除')], default=0, verbose_name='购物车商品状态'),
        ),
    ]
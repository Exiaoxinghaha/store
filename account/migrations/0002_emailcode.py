# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-26 04:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, verbose_name='验证码')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('email_type', models.SmallIntegerField(choices=[(0, '激活'), (1, '修改密码')], verbose_name='邮件类型')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-22 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable', '0036_auto_20180622_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='token',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]

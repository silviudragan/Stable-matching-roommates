# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-05-31 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stable', '0026_anunt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anunt',
            name='nume_expeditor',
        ),
    ]

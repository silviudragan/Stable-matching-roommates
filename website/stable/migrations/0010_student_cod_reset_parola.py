# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-17 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable', '0009_student_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cod_reset_parola',
            field=models.CharField(default='', max_length=8),
        ),
    ]

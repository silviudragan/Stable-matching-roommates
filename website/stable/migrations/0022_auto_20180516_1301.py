# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-05-16 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stable', '0021_student_facultate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camin',
            name='facultate',
            field=models.CharField(blank=True, choices=[('Biologie', 'Biologie'), ('Chimie', 'Chimie'), ('Drept', 'Drept'), ('Economie si Administrarea Afacerilor', 'Economie și Administrarea Afacerilor'), ('Educatie fizica si Sport', 'Educație fizică și Sport'), ('Filosofie si Stiinte Social-Politice', 'Filosofie și Științe Social-Politice'), ('Fizica', 'Fizică'), ('Geografie si Geologie', 'Geografie și Geologie'), ('Informatica', 'Informatică'), ('Istorie', 'Istorie'), ('Litere', 'Litere'), ('Matematica', 'Matematică'), ('Psihologie si Stiinte ale Educatiei', 'Psihologie și Științe ale Educației'), ('Teologie Ortodoxa', 'Teologie Ortodoxă'), ('Teologie Romano-Catolica', 'Teologie Romano-Catolică')], max_length=40),
        ),
        migrations.AlterField(
            model_name='student',
            name='facultate',
            field=models.CharField(choices=[('Biologie', 'Biologie'), ('Chimie', 'Chimie'), ('Drept', 'Drept'), ('Economie si Administrarea Afacerilor', 'Economie și Administrarea Afacerilor'), ('Educatie fizica si Sport', 'Educație fizică și Sport'), ('Filosofie si Stiinte Social-Politice', 'Filosofie și Științe Social-Politice'), ('Fizica', 'Fizică'), ('Geografie si Geologie', 'Geografie și Geologie'), ('Informatica', 'Informatică'), ('Istorie', 'Istorie'), ('Litere', 'Litere'), ('Matematica', 'Matematică'), ('Psihologie si Stiinte ale Educatiei', 'Psihologie și Științe ale Educației'), ('Teologie Ortodoxa', 'Teologie Ortodoxă'), ('Teologie Romano-Catolica', 'Teologie Romano-Catolică')], max_length=40),
        ),
    ]

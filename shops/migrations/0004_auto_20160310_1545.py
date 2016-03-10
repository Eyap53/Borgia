# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0003_auto_20160307_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productunit',
            name='type',
            field=models.CharField(choices=[('keg', 'fut'), ('liquor', 'alcool fort'), ('syrup', 'sirop'), ('soft', 'soft'), ('food', 'alimentaire'), ('meat', 'viande'), ('cheese', 'fromage'), ('side', 'accompagnement'), ('fictional_money', 'argent fictif')], default='keg', max_length=255),
        ),
    ]

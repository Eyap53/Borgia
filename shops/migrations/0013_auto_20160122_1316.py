# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-22 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_purchase'),
        ('shops', '0012_tap_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleProductFromContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.Container')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.Purchase')),
            ],
        ),
        migrations.AddField(
            model_name='singleproduct',
            name='purchase',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='finances.Purchase'),
            preserve_default=False,
        ),
    ]
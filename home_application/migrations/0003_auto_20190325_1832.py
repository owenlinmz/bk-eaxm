# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20190325_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostperformance',
            name='cpu',
            field=models.CharField(max_length=10, verbose_name='CPU\u4f7f\u7528\u7387'),
        ),
        migrations.AlterField(
            model_name='hostperformance',
            name='disk',
            field=models.CharField(max_length=10, verbose_name='\u78c1\u76d8\u4f7f\u7528\u7387'),
        ),
        migrations.AlterField(
            model_name='hostperformance',
            name='mem',
            field=models.CharField(max_length=10, verbose_name='\u5185\u5b58\u4f7f\u7528\u7387'),
        ),
    ]

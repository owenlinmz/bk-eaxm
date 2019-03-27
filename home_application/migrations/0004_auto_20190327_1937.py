# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_auto_20190325_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostinfo',
            name='bk_module_id',
            field=models.CharField(max_length=1000, verbose_name='\u6240\u5c5e\u6a21\u5757'),
        ),
        migrations.AlterField(
            model_name='hostinfo',
            name='bk_set_id',
            field=models.CharField(max_length=1000, verbose_name='\u6240\u5c5e\u96c6\u7fa4'),
        ),
    ]

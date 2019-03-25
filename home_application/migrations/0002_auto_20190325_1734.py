# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostinfo',
            name='bk_os_name',
            field=models.CharField(max_length=50, verbose_name='\u7cfb\u7edf\u540d'),
        ),
    ]

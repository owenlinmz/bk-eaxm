# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('bk_host_innerip', models.CharField(max_length=20, serialize=False, verbose_name='IP\u5730\u5740', primary_key=True)),
                ('bk_host_name', models.CharField(max_length=50, verbose_name='\u4e3b\u673a\u540d')),
                ('bk_os_name', models.CharField(max_length=30, verbose_name='\u7cfb\u7edf\u540d')),
                ('bk_inst_name', models.CharField(max_length=30, verbose_name='\u4e91\u533a\u57df\u540d\u79f0')),
                ('bk_biz_id', models.IntegerField(verbose_name='\u4e1a\u52a1ID')),
                ('bk_cloud_id', models.IntegerField(verbose_name='\u4e91\u533a\u57dfID')),
                ('bk_set_id', models.CharField(max_length=100, verbose_name='\u6240\u5c5e\u96c6\u7fa4')),
                ('bk_module_id', models.CharField(max_length=100, verbose_name='\u6240\u5c5e\u6a21\u5757')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
        ),
        migrations.CreateModel(
            name='HostPerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mem', models.IntegerField(verbose_name='\u5185\u5b58\u4f7f\u7528\u7387')),
                ('disk', models.IntegerField(verbose_name='\u78c1\u76d8\u4f7f\u7528\u7387')),
                ('cpu', models.IntegerField(verbose_name='CPU\u4f7f\u7528\u7387')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664')),
                ('check_time', models.DateTimeField(auto_now=True, verbose_name='\u68c0\u6d4b\u65f6\u95f4')),
                ('bk_host_innerip', models.ForeignKey(to='home_application.HostInfo', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('bk_biz_id', models.IntegerField(verbose_name='\u4e1a\u52a1ID')),
                ('bk_biz_name', models.CharField(max_length=50, verbose_name='\u4e1a\u52a1\u540d\u79f0')),
                ('user_name', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d')),
                ('ip', models.CharField(max_length=500, verbose_name='IP')),
                ('job_id', models.IntegerField(verbose_name='\u4f5c\u4e1a\u6a21\u7248ID')),
                ('job_instance_id', models.IntegerField(verbose_name='\u4f5c\u4e1a\u5b9e\u4f8bID')),
                ('operate_time', models.DateTimeField(verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
                ('job_status', models.CharField(max_length=20, verbose_name='\u4f5c\u4e1a\u72b6\u6001')),
                ('job_log', models.CharField(max_length=1000, verbose_name='\u4f5c\u4e1a\u65e5\u5fd7')),
            ],
        ),
    ]

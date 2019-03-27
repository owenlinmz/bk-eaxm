# -*- coding: utf-8 -*-
from django.db import models


class JobHistory(models.Model):
    id = models.AutoField(u"ID", primary_key=True)
    bk_biz_id = models.IntegerField(u'业务ID', null=False)
    bk_biz_name = models.CharField(u'业务名称', null=False, max_length=50)
    user_name = models.CharField(u'用户名', null=False, max_length=50)
    ip = models.CharField(u"IP", null=False, max_length=500)
    job_id = models.IntegerField(u'作业模版ID', null=False)
    job_instance_id = models.IntegerField(u'作业实例ID', null=False)
    operate_time = models.DateTimeField(u'操作时间', null=False)
    job_status = models.CharField(u'作业状态', null=False, max_length=20)
    job_log = models.CharField(u'作业日志', null=False, max_length=1000)


status_map = {
    1: u'未执行',
    2: u'正在执行',
    3: u'执行成功',
    4: u'执行失败'
}


class HostInfo(models.Model):
    bk_host_innerip = models.CharField(u'IP地址', max_length=20, primary_key=True, null=False)
    bk_host_name = models.CharField(u'主机名', max_length=50)
    bk_os_name = models.CharField(u'系统名', max_length=50)
    bk_inst_name = models.CharField(u'云区域名称', max_length=30)
    bk_biz_id = models.IntegerField(u'业务ID')
    bk_cloud_id = models.IntegerField(u'云区域ID')
    bk_set_id = models.CharField(u'所属集群', max_length=1000)
    bk_module_id = models.CharField(u'所属模块', max_length=1000)
    is_delete = models.BooleanField(u'是否删除', default=False)


class HostPerformance(models.Model):
    bk_host_innerip = models.ForeignKey(HostInfo, max_length=20, on_delete=models.CASCADE)
    mem = models.CharField(u'内存使用率', max_length=10)
    disk = models.CharField(u'磁盘使用率', max_length=10)
    cpu = models.CharField(u'CPU使用率', max_length=10)
    is_delete = models.BooleanField(u'是否删除', default=False)
    check_time = models.DateTimeField(u'检测时间', auto_now=True)

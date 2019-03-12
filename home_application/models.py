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

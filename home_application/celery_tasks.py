# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
import json

import requests
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger
from conf.default import BK_PAAS_HOST, APP_ID, APP_TOKEN
from home_application.models import JobHistory


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    import time
    time.sleep(20)
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week='*'))
def get_job_instance_status():
    logger.info(u"已启动作业状态查询")
    all_history = JobHistory.objects.all()
    for obj in all_history:
        if obj.job_status not in [3, 4]:
            url_status = BK_PAAS_HOST + '/api/c/compapi/v2/job/get_job_instance_status/'
            url_log = BK_PAAS_HOST + '/api/c/compapi/v2/job/get_job_instance_log/'
            params = {
                "bk_app_code": APP_ID,
                "bk_app_secret": APP_TOKEN,
                "bk_username": "admin",
                "bk_biz_id": obj.bk_biz_id,
                "job_instance_id": obj.job_instance_id
            }
            response_status = requests.post(url_status, json.dumps(params), verify=False)
            response_log = requests.post(url_log, json.dumps(params), verify=False)
            data_status = json.loads(response_status.content)
            data_log = json.loads(response_log.content)
            if data_status['result']:
                history_obj = JobHistory.objects.get(bk_biz_id=obj.bk_biz_id, job_instance_id=obj.job_instance_id)
                history_obj.job_status = data_status['data']['job_instance']['status']
                if data_log['result']:
                    history_obj.job_log = json.dumps(data_log['data'])
                    history_obj.save()

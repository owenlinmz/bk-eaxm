# -*- coding: utf-8 -*-
import json
import time

import requests
from django.http import JsonResponse

from account.decorators import login_exempt
from common.mymako import render_mako_context
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.celery_tasks import get_job_instance_status
from models import JobHistory


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    """
    测试
    """
    return render_mako_context(request, '/home_application/test.html')


def history(request):
    get_job_instance_status()
    return render_mako_context(request, '/home_application/history.html')


@login_exempt
def get_biz(request):
    url = BK_PAAS_HOST + '/api/c/compapi/v2/cc/search_business/'
    params = {
        'bk_app_code': APP_ID,
        'bk_app_secret': APP_TOKEN,
        'bk_username': 'admin',
        "fields": [
            "bk_biz_name", "bk_biz_id"
        ],
        "condition": {},
        "page": {
            "start": 0,
            "limit": 200
        }
    }
    response = requests.post(url, json.dumps(params), verify=False)
    return JsonResponse(json.loads(response.content))


@login_exempt
def get_set(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    url = BK_PAAS_HOST + '/api/c/compapi/v2/cc/search_set/'
    params = {
        'bk_app_code': APP_ID,
        'bk_app_secret': APP_TOKEN,
        'bk_username': 'admin',
        'bk_biz_id': bk_biz_id,
        "fields": [
            "bk_set_name", "bk_set_id"
        ],
        "condition": {},
        "page": {
            "start": 0,
            "limit": 200
        }
    }
    response = requests.post(url, json.dumps(params), verify=False)
    return JsonResponse(json.loads(response.content))


@login_exempt
def search_host(request):
    url = BK_PAAS_HOST + '/api/c/compapi/v2/cc/search_host/'
    bk_biz_id = int(request.GET.get('bk_biz_id'))
    bk_set_id = int(request.GET.get('bk_set_id'))
    params = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": "admin",
        "bk_biz_id": bk_biz_id,
        "condition": [
            {
                "bk_obj_id": "set",
                "fields": [
                    "bk_set_name",
                    "bk_set_id"
                ],
                "condition": [
                    {
                        "field": "bk_set_id",
                        "operator": "$eq",
                        "value": bk_set_id
                    }
                ]
            }
        ]
    }
    if not bk_set_id:
        params['condition'].pop('condition')
    response = requests.post(url, json.dumps(params), verify=False)
    return JsonResponse(json.loads(response.content))


@login_exempt
def execute_job(request):
    url = BK_PAAS_HOST + '/api/c/compapi/v2/job/execute_job/'
    data = json.loads(request.body)
    bk_biz_id = int(data['bk_biz_id'])
    ip_list = data['ip_list']
    for ip in ip_list:
        ip['bk_cloud_id'] = int(ip['bk_cloud_id'])
    params = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": "admin",
        "bk_biz_id": bk_biz_id,
        "bk_job_id": 1,
        "global_vars": [
            {
                "step_ids": [
                    1
                ],
                "description": "",
                "type": 2,
                "id": 1,
                "name": "id-201934122211263",
                "ip_list": ip_list
            }
        ]
    }
    ip_array = []
    response = requests.post(url, json.dumps(params), verify=False)
    data = json.loads(response.content)
    if data['result']:
        for ip in ip_list:
            ip_array.append(ip['ip'])
        create_data = {
            'bk_biz_id': bk_biz_id,
            'bk_biz_name': data['data']['job_instance_name'],
            'user_name': 'admin',
            'ip': ','.join(ip_array),
            'job_id': 1,
            'job_instance_id': data['data']['job_instance_id'],
            'operate_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'job_status': 2,
            'job_log': ''
        }
        JobHistory.objects.create(**create_data)
    return JsonResponse(json.loads(response.content))


def search_job_history_in_db(request):
    bk_biz_id = int(request.GET.get('bk_biz_id'))
    history_set = JobHistory.objects.filter(bk_biz_id=bk_biz_id)
    return_list = []
    from models import status_map
    for obj in history_set:
        return_list.append({
            'bk_biz_id': obj.bk_biz_id,
            'user_name': obj.user_name,
            'job_id': obj.job_id,
            'operation_time': obj.operate_time,
            'host': obj.ip,
            'job_status': status_map[int(obj.job_status)],
            'job_log': obj.job_log,
            'job_instance_id': obj.job_instance_id
        })
    return JsonResponse({'data': return_list})

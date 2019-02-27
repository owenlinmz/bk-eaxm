# -*- coding: utf-8 -*-
import json

import requests
from django.http import JsonResponse

from account.decorators import login_exempt
from common.mymako import render_mako_context
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST


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

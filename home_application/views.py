# -*- coding: utf-8 -*-
import datetime
import time
import base64

from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context
from common.mymako import render_json
from home_application.celery_tasks import get_job_instance_status
from models import JobHistory, HostPerformance
from common_esb import *
from models import HostInfo
from django.forms.models import model_to_dict


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


def history(request):
    get_job_instance_status()
    return render_mako_context(request, '/home_application/history.html')


def performance(request):
    return render_mako_context(request, '/home_application/performance.html')


def test(request):
    return render_json({"result": True, "message": "success", "data": request.user.username})


def get_biz(request):
    client = get_client_by_request(request)
    res = search_business(client, 'admin')
    return render_json(res)


def get_set(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    client = get_client_by_request(request)
    res = search_set(client, 'admin', bk_biz_id)
    return render_json(res)


# def search_host(request):
#     bk_biz_id = request.GET.get('bk_biz_id')
#     bk_set_id = request.GET.get('bk_set_id')
#     client = get_client_by_request(request)
#     res = get_host_by_biz_and_set(client, 'admin', bk_biz_id, bk_set_id)
#     # 处理主机信息
#     final_res = []
#     for item in res['data']:
#         item['host']['bk_inst_name'] = item['host']['bk_cloud_id'][0]['bk_inst_name']
#         final_res.append(item['host'])
#
#     return render_json(final_res)


def execute_job(request):
    data = json.loads(request.body)
    client = get_client_by_request(request)
    res = execute_job_esb(client, 'admin', data)
    ip_array = []
    if res['data']:
        for ip in data['ip_list']:
            ip_array.append(ip['ip'])
        create_data = {
            'bk_biz_id': data['bk_biz_id'],
            'bk_biz_name': res['data']['job_instance_name'],
            'user_name': 'admin',
            'ip': ','.join(ip_array),
            'job_id': 1,
            'job_instance_id': res['data']['job_instance_id'],
            'operate_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'job_status': 2,
            'job_log': ''
        }
        JobHistory.objects.create(**create_data)
    return render_json(res)


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


def get_performance(request):
    data = json.loads(request.body)
    client = get_client_by_request(request)
    script_content = '''#!/bin/bash
    MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
    DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
    CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "$DATE|$MEMORY|$DISK|$CPU"
    '''
    res = fast_execute_script(client, 'admin', data, base64.b64encode(script_content))
    time.sleep(2)
    if res['data']:
        params = {}
        params.update({'bk_biz_id': data['bk_biz_id'], 'job_instance_id': res['data']['job_instance_id']})
        res = get_job_instance_log(client, 'admin', params)

        # 处理性能数据
        try:
            pfm_data = res['data'][0]['step_results'][0]['ip_logs']
        except KeyError:
            pfm_data = []
        for item in pfm_data:
            result = item['log_content'].split('|')
            check_time = result[0]
            mem = result[1]
            disk = result[2]
            cpu = result[3]
            ip = item['ip']
            host_info = HostInfo.objects.get(bk_host_innerip=ip)
            HostPerformance.objects.create(
                bk_host_innerip=host_info,
                check_time=datetime.datetime.strptime(check_time, "%Y-%m-%d %H:%M:%S"),
                mem=mem,
                disk=disk,
                cpu=cpu
            )
        return render_json({'result': True})
    return render_json({'result': False})


def search_host(request):
    params = json.loads(request.body)
    bk_biz_id = params.get('bk_biz_id')
    client = get_client_by_request(request)
    res = get_host_by_biz_and_set(client, 'admin', bk_biz_id)
    host_write_into_db(res, bk_biz_id)

    # 处理无效的参数
    params = pop_useless_params(params)

    result = []
    host_info_list = HostInfo.objects.filter(**params)

    # 查询性能数据
    for host_info in host_info_list:
        host_info_dict = model_to_dict(host_info)
        host_performance = HostPerformance.objects.filter(bk_host_innerip=host_info_dict['bk_host_innerip']).order_by(
            'check_time').last()
        if host_performance:
            host_info_dict.update(model_to_dict(host_performance, fields=['bk_host_innerip', 'mem', 'disk', 'cpu']))
        else:
            host_info_dict.update({
                'mem': '--',
                'disk': '--',
                'cpu': '--'
            })
        result.append(host_info_dict)
    return render_json({'data': result})


def host_write_into_db(result, bk_biz_id):
    for item in result['data']:
        bk_set_id = set()
        bk_module_id = set()
        for v in item['module']:
            bk_set_id.add(v['bk_set_id'])
            bk_module_id.add(v['bk_module_id'])
        params = {
            'bk_host_innerip': item['host']['bk_host_innerip'],
            'bk_host_name': item['host']['bk_host_name'],
            'bk_os_name': item['host']['bk_os_name'],
            'bk_inst_name': item['host']['bk_cloud_id'][0]['bk_inst_name'],
            'bk_module_id': bk_module_id,
            'bk_cloud_id': item['host']['bk_cloud_id'][0]['id'],
            'bk_set_id': bk_set_id,
            'bk_biz_id': bk_biz_id
        }
        if HostInfo.objects.filter(bk_host_innerip=params['bk_host_innerip']):
            HostInfo.objects.filter(bk_host_innerip=params['bk_host_innerip']).update(**params)
        else:
            HostInfo.objects.create(**params)


def display_performance(request):
    def generate_data(pfm_list):
        xAxis = []
        series = []
        mem = []
        cpu = []
        disk = []
        for host_pfm in pfm_list:
            xAxis.append(host_pfm.check_time.strftime("%Y-%m-%d %H:%M:%S"))
            mem.append(float(host_pfm.mem.strip('%')))
            cpu.append(float(host_pfm.cpu.strip('%\n')))
            disk.append(float(host_pfm.disk.strip('%')))
        series.append({
            'name': 'mem',
            'type': 'line',
            'data': mem
        })
        series.append({
            'name': 'cpu',
            'type': 'line',
            'data': cpu
        })
        series.append({
            'name': 'disk',
            'type': 'line',
            'data': disk
        })
        return {
            "xAxis": xAxis,
            "series": series
        }

    params = pop_useless_params(json.loads(request.body))

    result = []
    host_pfm_list = HostPerformance.objects.filter(**params)
    if params.get('bk_host_innerip__in', None):
        for ip in params['bk_host_innerip__in']:
            single_host_pfm_list = host_pfm_list.filter(bk_host_innerip=ip)
            result.append(generate_data(single_host_pfm_list))
    else:
        result.append(generate_data(host_pfm_list))

    return render_json({'data': result})


def pop_useless_params(params):
    pop_keys = []
    for key, value in params.items():
        if value == '':
            pop_keys.append(key)
        if key.endswith('__in'):
            params[key] = value.split(',')
    for pop in pop_keys:
        params.pop(pop)
    return params

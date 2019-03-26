# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^api/test/$', 'test'),
    (r'^history/$', 'history'),
    (r'^performance/$', 'performance'),
    (r'^get_set/$', 'get_set'),
    (r'^get_biz/$', 'get_biz'),
    (r'^search_host/$', 'search_host'),
    (r'^execute_job/$', 'execute_job'),
    (r'^get_job_instance_status/$', 'execute_job'),
    (r'^search_job_history_in_db/$', 'search_job_history_in_db'),
    (r'^get_performance/$', 'get_performance'),
    (r'^display_performance/$', 'display_performance'),
    (r'^get_new_pfm/$', 'get_new_pfm'),
    (r'^switch_performance/$', 'switch_performance')
)

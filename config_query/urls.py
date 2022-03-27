# -*- coding: utf-8 -*-
from django.urls import path

from config_query import local_views

local_urlpatterns = (
    path("local/business/", local_views.business),
    path("local/sets_of_business/<int:bk_biz_id>/", local_views.sets_of_business),
    path("local/modules_of_set/<int:bk_biz_id>/<int:bk_set_id>/", local_views.modules_of_set),
    path("local/filter_hosts/", local_views.filter_hosts),
    path("local/host_base_info/<int:bk_host_id>/", local_views.host_base_info),
    path("local/sync_host_data/", local_views.sync_host_data),
    path("local/search_host_files/", local_views.search_host_files),
    path("local/backup_host_files/", local_views.backup_host_files),
    path("local/backup_records/", local_views.backup_records),
    path("local/search_host_files_result/<str:result_id>/", local_views.search_host_files_result),
)

urlpatterns = ()

urlpatterns += local_urlpatterns

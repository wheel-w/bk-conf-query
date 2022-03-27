# -*- coding: utf-8 -*-
from django.urls import path

from config_query import local_views

local_urlpatterns = (
    path("business/", local_views.business),
    path("sets_of_business/<int:bk_biz_id>/", local_views.sets_of_business),
    path("modules_of_set/<int:bk_biz_id>/<int:bk_set_id>/", local_views.modules_of_set),
    path("filter_hosts/", local_views.filter_hosts),
    path("host_base_info/<int:bk_host_id>/", local_views.host_base_info),
    path("sync_host_data/", local_views.sync_host_data),
    path("search_host_files/", local_views.search_host_files),
    path("backup_host_files/", local_views.backup_host_files),
    path("backup_records/", local_views.backup_records),
    path("search_host_files_result/<str:result_id>/", local_views.search_host_files_result),
)

urlpatterns = ()

urlpatterns += local_urlpatterns

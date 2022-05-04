# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import path
from iam import IAM
from iam.contrib.django.dispatcher import DjangoBasicResourceApiDispatcher

from blueapps.account.decorators import login_exempt
from config_query import local_views
from config_query.provider import (
    BusinessResourceProvider,
    HostResourceProvider,
    ModuleResourceProvider,
    SetResourceProvider,
)

iam = IAM(
    settings.APP_CODE, settings.SECRET_KEY, bk_apigateway_url=settings.BK_APIGATEWAY_URL
)

dispatcher = DjangoBasicResourceApiDispatcher(iam, settings.APP_CODE)
dispatcher.register("bk_biz", BusinessResourceProvider())
dispatcher.register("bk_set", SetResourceProvider())
dispatcher.register("bk_module", ModuleResourceProvider())
dispatcher.register("bk_host", HostResourceProvider())

urlpatterns = (path("resource/api/v1/", dispatcher.as_view([login_exempt])),)

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
    path(
        "search_host_files_result/<str:result_id>/",
        local_views.search_host_files_result,
    ),
    path(
        "make_host_apply_url/<int:bk_biz_id>/<int:bk_set_id>/<int:bk_module_id>/<int:bk_host_id>/",
        local_views.make_host_apply_url,
    ),
)

urlpatterns += local_urlpatterns

# -*- coding: utf-8 -*-
import django_filters

from config_query.models import Host


class HostFilter(django_filters.FilterSet):
    bk_host_id = django_filters.NumberFilter(lookup_expr="exact")
    bk_host_name = django_filters.CharFilter(lookup_expr="icontains")
    bk_host_innerip = django_filters.CharFilter(lookup_expr="startswith")
    bk_host_outerip = django_filters.CharFilter(lookup_expr="startswith")
    operator = django_filters.CharFilter(lookup_expr="icontains")
    bk_bak_operator = django_filters.CharFilter(lookup_expr="icontains")
    bk_cloud_id = django_filters.NumberFilter(lookup_expr="exact")
    bk_biz_id = django_filters.CharFilter(lookup_expr="contains")
    bk_set_id = django_filters.CharFilter(lookup_expr="contains")
    bk_module_id = django_filters.CharFilter(lookup_expr="contains")

    class Meta:
        model = Host
        fields = "__all__"

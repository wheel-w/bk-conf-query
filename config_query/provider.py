# -*- coding: utf-8 -*-
import logging

from django.db.models import Q
from iam.resource.provider import ListResult, ResourceProvider

from config_query.models import Business, Host, Module, Set

logger = logging.getLogger("root")


class BusinessResourceProvider(ResourceProvider):
    """
    业务资源类型
    """

    def list_attr(self, **options):
        logger.info("business list_attr")
        return ListResult(results=[])

    def list_attr_value(self, filter, page, **options):
        logger.info("business list_attr_value")
        return ListResult(results=[])

    def list_instance(self, filter, page, **options):
        queryset = Business.objects.all()

        results = [
            {"id": str(biz.bk_biz_id), "display_name": biz.bk_biz_name}
            for biz in queryset[page.slice_from : page.slice_to]
        ]

        logger.info(f"business list_instance {results}")
        return ListResult(results=results, count=len(queryset))

    def fetch_instance_info(self, filter, **options):
        ids = []
        if filter.ids:
            ids = [int(i) for i in filter.ids]

        results = [
            {"id": str(biz.bk_biz_id), "display_name": biz.bk_biz_name}
            for biz in Business.objects.filter(bk_biz_id__in=ids)
        ]
        logger.info(f"business fetch_instance_info {results}")
        return ListResult(results=results, count=len(results))

    def list_instance_by_policy(self, filter, page, **options):
        logger.info("business list_instance_by_policy")
        return ListResult(results=[])

    def search_instance(self, filter, page, **options):
        keyword = filter["keyword"]
        biz_filter = Q(bk_biz_name__contains=keyword)
        try:
            int(keyword)
            biz_filter |= Q(bk_biz_id=keyword)
        except ValueError:
            logger.info("关键字不是业务ID")
        queryset = Business.objects.filter(biz_filter)
        results = [
            {"id": biz.bk_biz_id, "display_name": biz.bk_biz_name}
            for biz in queryset[page.slice_from : page.slice_to]
        ]
        logger.info("business search_instance")
        return ListResult(results=results, count=len(results))


class SetResourceProvider(ResourceProvider):
    """
    集群资源类型
    """

    def list_attr(self, **options):
        logger.info("set list_attr")
        return ListResult(results=[])

    def list_attr_value(self, filter, page, **options):
        logger.info("set list_attr_value")
        return ListResult(results=[])

    def list_instance(self, filter, page, **options):
        logger.info(f"set list_instance{filter}")
        parent_id = filter.parent["id"]
        queryset = Set.objects.all().filter(bk_biz_id=parent_id)
        results = [
            {"id": str(sett.bk_set_id), "display_name": sett.bk_set_name}
            for sett in queryset[page.slice_from : page.slice_to]
        ]
        logger.info(f"set list_instance {results}")
        return ListResult(results=results, count=len(queryset))

    def fetch_instance_info(self, filter, **options):
        logger.info(f"set fetch_instance_info{filter}")
        if "*" in filter.ids:
            queryset = Set.objects.all().filter(bk_biz_id=filter.parent["id"])
        else:
            ids = []
            if filter.ids:
                ids = [int(i) for i in filter.ids]
            queryset = Set.objects.filter(bk_set_id__in=ids)

        results = [
            {"id": str(sett.bk_set_id), "display_name": sett.bk_set_name}
            for sett in queryset
        ]
        logger.info(f"set fetch_instance_info {results}")
        return ListResult(results=results, count=len(results))

    def list_instance_by_policy(self, filter, page, **options):
        logger.info("set list_instance_by_policy")
        return ListResult(results=[])


class ModuleResourceProvider(ResourceProvider):
    """
    模块资源类型
    """

    def list_attr(self, **options):
        logger.info("module list_attr")
        return ListResult(results=[])

    def list_attr_value(self, filter, page, **options):
        logger.info("module list_attr_value")
        return ListResult(results=[])

    def list_instance(self, filter, page, **options):
        parent_id = filter.parent["id"]
        queryset = Module.objects.all().filter(bk_set_id=parent_id)
        results = [
            {"id": str(module.bk_module_id), "display_name": module.bk_module_name}
            for module in queryset[page.slice_from : page.slice_to]
        ]
        logger.info(f"module list_instance{results}")
        return ListResult(results=results, count=len(queryset))

    def fetch_instance_info(self, filter, **options):
        ids = []
        if filter.ids:
            ids = [int(i) for i in filter.ids]

        results = [
            {"id": str(module.bk_module_id), "display_name": module.bk_module_id}
            for module in Module.objects.filter(bk_module_id__in=ids)
        ]
        logger.info(f"module fetch_instance_info{results}")
        return ListResult(results=results, count=len(results))

    def list_instance_by_policy(self, filter, page, **options):
        logger.info("module list_instance_by_policy")
        return ListResult(results=[])


class HostResourceProvider(ResourceProvider):
    """
    主机资源类型
    """

    def list_attr(self, **options):
        logger.info("host list_attr")
        return ListResult(results=[])

    def list_attr_value(self, filter, page, **options):
        logger.info("host list_attr_value")
        return ListResult(results=[])

    def list_instance(self, filter, page, **options):
        parent_id = filter.parent["id"]
        queryset = Host.objects.all().filter(bk_module_id__contains=f"{parent_id},")
        results = [
            {
                "id": str(host.bk_host_id),
                "display_name": f"[{host.bk_cloud_id}]{host.bk_host_innerip}",
            }
            for host in queryset[page.slice_from : page.slice_to]
        ]
        logger.info(f"host list_instance{results}")
        return ListResult(results=results, count=len(queryset))

    def fetch_instance_info(self, filter, **options):
        ids = []
        if filter.ids:
            ids = [int(i) for i in filter.ids]

        results = [
            {
                "id": str(host.bk_host_id),
                "display_name": f"[{host.bk_cloud_id}]{host.bk_host_innerip}",
            }
            for host in Host.objects.filter(bk_host_id__in=ids)
        ]
        logger.info(f"host fetch_instance_info{results}")
        return ListResult(results=results, count=len(results))

    def list_instance_by_policy(self, filter, page, **options):
        logger.info("host list_instance_by_policy")
        return ListResult(results=[])

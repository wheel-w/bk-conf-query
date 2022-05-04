# -*- coding: utf-8 -*-
import logging
import sys

from django.conf import settings
from iam import IAM, Action, MultiActionRequest, Request, Resource, Subject
from iam.apply.models import (
    ActionWithResources,
    Application,
    RelatedResourceType,
    ResourceInstance,
    ResourceNode,
)

logger = logging.getLogger("iam")
logger.setLevel(logging.DEBUG)

debug_hanler = logging.StreamHandler(sys.stdout)
debug_hanler.setFormatter(
    logging.Formatter("%(levelname)s [%(asctime)s] [IAM] %(message)s")
)
logger.addHandler(debug_hanler)


class Permission(object):
    def __init__(self):
        self._iam = IAM(
            settings.APP_CODE,
            settings.SECRET_KEY,
            bk_apigateway_url=settings.BK_APIGATEWAY_URL,
        )

    def _make_request_without_resources(self, username, action_id):
        request = Request(
            settings.APP_CODE,
            Subject("user", username),
            Action(action_id),
            None,
            None,
        )
        return request

    def _make_request_with_resources(self, username, action_id, resources):
        request = Request(
            settings.APP_CODE,
            Subject("user", username),
            Action(action_id),
            resources,
            None,
        )
        return request

    def make_resource_application(
        self, action_id, resource_type, resource_id, resource_name
    ):
        # 1. make application
        # 这里支持带层级的资源, 例如 biz: 1/set: 2/host: 3
        # 如果不带层级, list中只有对应资源实例
        instance = ResourceInstance(
            [ResourceNode(resource_type, resource_id, resource_name)]
        )
        # 同一个资源类型可以包含多个资源
        related_resource_type = RelatedResourceType(
            settings.APP_CODE, resource_type, [instance]
        )
        action = ActionWithResources(action_id, [related_resource_type])

        actions = [
            action,
        ]
        application = Application(settings.APP_CODE, actions)
        return application

    def generate_apply_url(self, bk_token, application):
        """
        处理无权限 - 跳转申请列表
        """
        # 2. get url
        ok, message, url = self._iam.get_apply_url(application, bk_token)
        if not ok:
            logger.error("iam generate apply url fail: %s", message)
            return settings.IAM_APP_URL
        return url

    def is_bk_super_user(self, username):
        """
        判断是否是超级管理员
        """
        request = self._make_request_without_resources(username, "bk_super_user")
        is_allowed = self._iam.is_allowed(request)
        url = ""
        if not is_allowed:
            actions = [{"id": "bk_super_user", "related_resource_types": []}]
            application = {"system": settings.APP_CODE, "actions": actions}
            url = self.generate_apply_url(username, application)
        return is_allowed, url

    def is_bk_biz_manage(self, username, bk_biz_id):
        """
        判断是否有当前业务权限
        """
        r = Resource(settings.APP_CODE, "bk_biz", str(bk_biz_id), {})
        resources = [r]
        request = self._make_request_with_resources(
            username, "bk_biz_manage", resources
        )
        is_allowed = self._iam.is_allowed(request)
        url = ""
        if not is_allowed:
            application = self.make_resource_application(
                "bk_biz_manage", "bk_biz", str(bk_biz_id), "业务拓扑"
            )
            url = self.generate_apply_url(username, application)
        return is_allowed, url

    def is_bk_host_manage(self, username, bk_host_id):
        """
        判断是否有主机资源权限
        """
        r = Resource(
            settings.APP_CODE,
            "bk_host",
            str(bk_host_id),
            {"_bk_iam_path_": "/bk_biz,215/bk_set,2000000943/bk_module,2000000991/"},
        )
        resources = [r]
        request = self._make_request_with_resources(
            username, "bk_host_manage", resources
        )
        return self._iam.is_allowed(request)

    def batch_auth_business(self, username, queryset):
        """
        批量鉴权业务
        """
        subject = Subject("user", username)
        action = Action("bk_biz_manage")
        resources = []
        for biz in queryset:
            resources.append(
                [
                    Resource(
                        settings.APP_CODE,
                        "bk_biz",
                        str(biz.bk_biz_id),
                        {"_bk_iam_path_": f"/bk_biz,{biz.bk_biz_id}/bk_set,*/"},
                    )
                ]
            )
        request = MultiActionRequest(settings.APP_CODE, subject, [action], [], None)

        return self._iam.batch_resource_multi_actions_allowed(request, resources)

    def batch_auth_host(self, username, queryset):
        """
        批量鉴权主机
        """
        subject = Subject("user", username)
        action = Action("bk_host_manage")
        resources = []
        for host in queryset:
            bk_host_id = host.bk_host_id
            bk_biz_id = host.bk_biz_id.replace(",", "")
            bk_set_id = host.bk_set_id.split(",")[0]
            bk_module_id = host.bk_module_id.split(",")[0]
            resources.append(
                [
                    Resource(
                        settings.APP_CODE,
                        "bk_host",
                        str(bk_host_id),
                        {
                            "_bk_iam_path_": f"/bk_biz,{bk_biz_id}/bk_set,{bk_set_id}/bk_module,{bk_module_id}/,{bk_host_id}/"
                            # noqa
                        },
                    )
                ]
            )
        if not resources:
            resources = [[]]
        request = MultiActionRequest(settings.APP_CODE, subject, [action], [], None)
        return self._iam.batch_resource_multi_actions_allowed(request, resources)

    def make_host_apply_url(
        self, username, bk_biz_id, bk_set_id, bk_module_id, bk_host_id
    ):
        """
        生成主机资源的权限跳转链接
        """
        instance = ResourceInstance(
            [
                ResourceNode("bk_biz", bk_biz_id, "业务"),
                ResourceNode("bk_set", bk_set_id, "集群"),
                ResourceNode("bk_module", bk_module_id, "模块"),
                ResourceNode("bk_host", bk_host_id, "主机"),
            ]
        )
        # 同一个资源类型可以包含多个资源
        related_resource_type = RelatedResourceType(
            settings.APP_CODE, "bk_host", [instance]
        )
        action = ActionWithResources("bk_host_manage", [related_resource_type])

        actions = [
            action,
        ]
        application = Application(settings.APP_CODE, actions)
        url = self.generate_apply_url(username, application)

        return url

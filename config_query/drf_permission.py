# -*- coding: utf-8 -*-
from rest_framework import permissions

from config_query.base import SyncCommand
from config_query.iam_permission import Permission

iam_permissions = Permission()


class IsBizAccessIam(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # 获取参数
        kwargs = {**view.kwargs, **request.data}

        # 判断是否是系统管理员
        is_super_user, permission_url = iam_permissions.is_bk_super_user(
            request.user.username
        )

        # 判断是否是系统管理员才能进行的操作
        # 同步全部业务数据
        if "value" in kwargs and kwargs["value"] == SyncCommand.SYNC_ALL:
            view.permission_url = permission_url
            view.status = 403
            return is_super_user

        # 判断是否有业务权限
        is_bk_biz_manage = False
        if "bk_biz_id" in kwargs and kwargs["bk_biz_id"]:
            is_bk_biz_manage, permission_url = iam_permissions.is_bk_biz_manage(
                request.user.username, kwargs["bk_biz_id"]
            )

        if is_super_user or is_bk_biz_manage:
            return True

        view.permission_url = permission_url
        view.status = 403
        return False

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.

        return True

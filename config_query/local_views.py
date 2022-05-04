# -*- coding: utf-8 -*-
from django.core.cache import caches
from rest_framework.decorators import api_view, permission_classes

from config_query import cmdb
from config_query.base import SyncCommand, SyncTaskStatus
from config_query.drf_permission import IsBizAccessIam
from config_query.filters import HostFilter
from config_query.iam_permission import Permission
from config_query.models import BackupHostFileRecord, Business, Host, Module, Set
from config_query.paginations import ConfigQueryLimitOffsetPagination
from config_query.response import ConfigQueryResponse
from config_query.serializers import (
    BackupHostFileRecordSerializer,
    JobBackupHostSerializer,
    JobSearchHostSerializer,
)
from config_query.tasks import (
    backup_host_files_task,
    search_host_files_task,
    sync_data_task,
    sync_single_data_task,
)

cache = caches["default"]
iam_permission = Permission()


# Create your views here.
@api_view(["GET"])
def business(request):
    """
    获取用户的所有业务名和业务ID
    """
    queryset = Business.objects.all()
    data = []
    is_super_user, _ = iam_permission.is_bk_super_user(request.user.username)
    # 如果是系统管理员解锁所有业务
    if is_super_user:
        for biz in queryset:
            data.append(
                {
                    "bk_biz_id": biz.bk_biz_id,
                    "bk_biz_name": biz.bk_biz_name,
                    "is_auth": True,
                }
            )
        return ConfigQueryResponse(data=data)

    # 普通人员进行业务批量鉴权,返回有无权限信息
    auth_biz = iam_permission.batch_auth_business(request.user.username, queryset)

    for biz in queryset:
        data.append(
            {
                "bk_biz_id": biz.bk_biz_id,
                "bk_biz_name": biz.bk_biz_name,
                "is_auth": auth_biz[str(biz.bk_biz_id)]["bk_biz_manage"],
            }
        )

    data.sort(key=sort_by_auth, reverse=True)

    return ConfigQueryResponse(data=data)


@api_view(["GET"])
@permission_classes([IsBizAccessIam])
def sets_of_business(request, bk_biz_id=None):
    """
    获取某个业务下的所有集群的集群名和集群ID
    """
    queryset = Set.objects.all().filter(bk_biz_id=bk_biz_id)

    data = []
    for bk_set in queryset:
        data.append(
            {
                "id": bk_set.bk_set_id,
                "level": 0,
                "name": bk_set.bk_set_name,
            }
        )

    return ConfigQueryResponse(data=data)


@api_view(["GET"])
@permission_classes([IsBizAccessIam])
def modules_of_set(request, bk_biz_id=None, bk_set_id=None):
    """
    获取某个集群下的所有模块的模块名称和模块ID
    """
    queryset = Module.objects.all().filter(bk_biz_id=bk_biz_id, bk_set_id=bk_set_id)
    data = []
    for module in queryset:
        data.append(
            {
                "id": f"module{module.bk_module_id}",
                "bk_module_id": module.bk_module_id,
                "name": module.bk_module_name,
            }
        )
    return ConfigQueryResponse(data=data)


@api_view(["POST"])
@permission_classes([IsBizAccessIam])
def filter_hosts(request):
    """
    根据参数获取对应的主机列表
    """

    params = {key: value for key, value in request.data.items() if value or value == 0}

    host_filter = HostFilter(data=params, queryset=Host.objects.all())
    page = ConfigQueryLimitOffsetPagination()
    queryset = page.paginate_queryset(host_filter.qs, request)
    is_super_user, _ = iam_permission.is_bk_super_user(request.user.username)
    data = []

    # 如果是系统管理员解锁所有业务
    if is_super_user:
        for host in queryset:
            data.append(
                {
                    "bk_host_id": host.bk_host_id,
                    "bk_biz_id": host.bk_biz_id,
                    "bk_set_id": host.bk_set_id,
                    "bk_module_id": host.bk_module_id,
                    "bk_host_name": host.bk_host_name,
                    "bk_host_innerip": host.bk_host_innerip,
                    "bk_host_outerip": host.bk_host_outerip,
                    "bk_cloud_id": host.bk_cloud_id,
                    "operator": host.operator,
                    "bk_bak_operator": host.bk_bak_operator,
                    "bk_os_type": host.bk_os_type,
                    "is_auth": True,
                }
            )
        return ConfigQueryResponse(data=data, count=page.count)
    if queryset:
        auth_host = iam_permission.batch_auth_host(request.user.username, queryset)
    for host in queryset:
        data.append(
            {
                "bk_host_id": host.bk_host_id,
                "bk_biz_id": host.bk_biz_id,
                "bk_set_id": host.bk_set_id,
                "bk_module_id": host.bk_module_id,
                "bk_host_name": host.bk_host_name,
                "bk_host_innerip": host.bk_host_innerip,
                "bk_host_outerip": host.bk_host_outerip,
                "bk_cloud_id": host.bk_cloud_id,
                "operator": host.operator,
                "bk_bak_operator": host.bk_bak_operator,
                "bk_os_type": host.bk_os_type,
                "is_auth": auth_host[str(host.bk_host_id)]["bk_host_manage"],
            }
        )
    data.sort(key=sort_by_auth, reverse=True)
    return ConfigQueryResponse(data=data, count=page.count)


@api_view(["GET"])
@permission_classes([IsBizAccessIam])
def host_base_info(request, bk_host_id=None):
    """
    获取主机详细信息
    """

    response = cmdb.get_host_base_info(request.user.username, bk_host_id=bk_host_id)

    return ConfigQueryResponse(data=response["data"])


@api_view(["POST"])
@permission_classes([IsBizAccessIam])
def sync_host_data(request):
    """
    启动同步数据库任务
    """
    command = request.data
    if command["value"] == SyncCommand.SYNC_ALL:
        sync_host_flag = cache.get("sync_all", SyncTaskStatus.IDLE)
        if sync_host_flag in [SyncTaskStatus.RUNNING, SyncTaskStatus.WAIT]:
            return ConfigQueryResponse(result=False)
        cache.set("sync_all", SyncTaskStatus.WAIT, timeout=1800)
        sync_data_task.delay(request.user.username)

    if command["value"] == SyncCommand.SYNC_SINGLE:
        sync_host_flag = cache.get(
            command["business"]["bk_biz_id"], SyncTaskStatus.IDLE
        )
        if sync_host_flag in [SyncTaskStatus.RUNNING, SyncTaskStatus.WAIT]:
            return ConfigQueryResponse(result=False)
        cache.set(command["business"]["bk_biz_id"], SyncTaskStatus.WAIT, timeout=1800)
        sync_single_data_task.delay(request.user.username, command["business"])

    return ConfigQueryResponse(result=True)


@api_view(["POST"])
def search_host_files(request):
    """
    搜索主机文件
    """
    serializer = JobSearchHostSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    async_result = search_host_files_task.delay(request.user.username, serializer.data)

    return ConfigQueryResponse(async_result.id)


@api_view(["GET"])
def search_host_files_result(request, result_id):
    result = cache.get(result_id)
    if result:
        return ConfigQueryResponse(data=result)
    return ConfigQueryResponse(result=False)


@api_view(["POST"])
def backup_host_files(request):
    """
    备份主机文件
    """
    serializer = JobBackupHostSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    if data["file_directory"] != "/data/wheel_test":
        message = "{}禁止备份".format(data["file_directory"])
        return ConfigQueryResponse(result=False, message=message)
    backup_host_files_task.delay(request.user.username, data)
    return ConfigQueryResponse()


@api_view(["GET"])
def backup_records(request):
    """
    获取备份记录
    """
    queryset = BackupHostFileRecord.objects.filter(
        backup_operator=request.user.username
    ).order_by("-backup_time")
    page = ConfigQueryLimitOffsetPagination()
    data = page.paginate_queryset(queryset, request)
    serializer = BackupHostFileRecordSerializer(data, many=True)
    return ConfigQueryResponse(data=serializer.data, count=page.count)


@api_view(["GET"])
def make_host_apply_url(request, bk_biz_id, bk_set_id, bk_module_id, bk_host_id):
    url = iam_permission.make_host_apply_url(
        request.user.username, bk_biz_id, bk_set_id, bk_module_id, bk_host_id
    )
    return ConfigQueryResponse(data=url)


def sort_by_auth(ele):
    return ele["is_auth"]

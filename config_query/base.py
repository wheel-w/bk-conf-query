# -*- coding: utf-8 -*-
import logging
import math
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait

from django.db import transaction

HTTP_GET = "GET"
HTTP_POST = "POST"
# 并发请求的最大线程数
MAX_WORKER = 50

logger = logging.getLogger("root")


class JobExecuteStatus:
    """
    job作业执行状态枚举
    """

    SUCCESS = 3
    FAILED = 4


class ScriptLanguage:
    """
    快速执行脚本，脚本语言类型枚举
    """

    SHELL = 1
    BAT = 2
    PERL = 3
    PYTHON = 4
    POWERSHELL = 5


class SyncTaskStatus:
    """
    同步数据库任务状态枚举
    """

    WAIT = "sync_wait"
    IDLE = "sync_idle"
    RUNNING = "sync_running"


class PageDataLimit:
    """
    分页拉取cmdb数据limit枚举
    """

    HOST_PAGE_LIMIT = 500
    TOPO_PAGE_LIMIT = 200


class SyncCommand:
    """
    同步业务数据命令枚举
    """

    SYNC_ALL = "sync_all"
    SYNC_SINGLE = "sync_single"


def get_page_data(username, request_method, bk_biz_id, page_size, key="info"):
    """
    获取有分页限制的API数据
    """
    params = {
        "bk_biz_id": bk_biz_id,
        "page": 1,
        "page_size": page_size,
    }
    res = request_method(username, params)["data"]
    page = math.ceil(res["count"] / page_size)
    result_list = []
    if page != 0:
        index = 1
        while True:
            result_list += res[key]

            if index == page:
                break
            index += 1
            params["page"] = index
            res = request_method(username, params)["data"]

    return result_list


class ApiRequestError(Exception):
    def __init__(self, message):
        self.message = "ApiRequestError: {}".format(message)

    def __str__(self):
        return self.message


def batch_request(
    func,
    params,
    get_data=lambda x: x["data"]["info"],
    get_count=lambda x: x["data"]["count"],
    page_size=500,
    page_param=lambda x, y: {"start": x, "limit": y},
):
    """
    并发请求接口
    :param func: 请求方法
    :param params: 请求参数
    :param get_data: 获取数据函数
    :param get_count: 获取总数函数
    :param page_size: 一次请求最大数量
    :param page_param: 分页参数，默认使用start/limit分页，例如：{"cur_page_param":"start", "page_size_param":"limit"}
    :return: 请求结果
    """
    # 请求第一次获取总数
    result = func(**page_param(1, 1), **params)

    if not result["result"]:
        message = "batch request api {} error,response {}".format(func, result)
        logger.error(message)
        raise ApiRequestError(message)

    count = get_count(result)
    page = math.ceil(count / page_size)

    # 封装请求参数
    param_list = []
    for current_page in range(1, page + 1):
        param_list.append({**page_param(current_page, page_size), **params})

    max_workers = MAX_WORKER if len(param_list) > MAX_WORKER else len(param_list)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        task_list = [pool.submit(func, **param) for param in param_list]

    wait(task_list, return_when=ALL_COMPLETED)
    data = []
    for task in task_list:
        if not get_data(task.result()):
            message = "batch request api {} error,response {}".format(
                func, task.result()
            )
            logger.exception()
            raise ApiRequestError(message)
        data += get_data(task.result())

    return data


@transaction.atomic
def bulk_create_or_update_delete(
    model, bk_biz_id, primary_key_name=None, online_data_dict=None, fields=[]
):
    """
    批量创建 更新 删除 数据库数据
    """
    db_data_dict = {
        getattr(inst, primary_key_name): inst
        for inst in model.objects.all().filter(bk_biz_id=bk_biz_id)
    }

    create_keys = online_data_dict.keys() - db_data_dict.keys()
    create_list = [online_data_dict[key] for key in create_keys]
    model.objects.bulk_create(create_list)

    update_keys = online_data_dict.keys() - create_list
    update_list = [online_data_dict[key] for key in update_keys]
    model.objects.bulk_update(update_list, fields=fields)

    delete_keys = db_data_dict.keys() - online_data_dict.keys()
    model.objects.filter(**{f"{primary_key_name}__in": delete_keys}).delete()

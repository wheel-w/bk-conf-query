# -*- coding: utf-8 -*-

import logging
import posixpath

from celery.task import task
from django.core.cache import caches

from config_query import cmdb, job
from config_query.base import (
    PageDataLimit,
    SyncTaskStatus,
    bulk_create_or_update_delete,
    get_page_data,
)
from config_query.models import BackupHostFileRecord, Business, Host, Module, Set

logger = logging.getLogger("celery")
cache = caches["default"]


@task()
def sync_data_task(username):
    """
    同步cmdb数据到数据库
    """
    sync_host_flag = cache.get("sync_all", SyncTaskStatus.IDLE)
    if sync_host_flag == SyncTaskStatus.RUNNING:
        logger.info("同步全部业务任务正在进行！！！")
        return

    cache.set("sync_all", SyncTaskStatus.RUNNING, timeout=1800)
    biz_list = cmdb.get_business_info(username)["data"]["info"]
    end_business = biz_list.pop()
    for business in biz_list:
        sync_single_data(username, business)
    sync_single_data(username, end_business, is_finished=True)


@task()
def sync_single_data_task(username, business):
    """
    同步单个业务的数据到数据库
    """
    sync_host_flag = cache.get(business["bk_biz_id"], SyncTaskStatus.IDLE)
    if sync_host_flag == SyncTaskStatus.RUNNING:
        logger.info(f"同步[{business['bk_biz_id']}]{business['bk_biz_name']}业务任务正在进行！！！")
        return

    cache.set(business["bk_biz_id"], SyncTaskStatus.RUNNING, timeout=1800)
    sync_single_data(username, business)
    cache.set(business["bk_biz_id"], SyncTaskStatus.IDLE, timeout=1800)


@task()
def sync_single_data(username, business, is_finished=False):
    """
    同步指定业务的数据到数据库
    """
    # 保存业务信息到业务表
    db_business = {"bk_biz_id": business["bk_biz_id"], "bk_biz_name": business["bk_biz_name"]}
    Business.objects.update_or_create(bk_biz_id=business["bk_biz_id"], defaults=db_business)

    # 保存集群信息到集群表
    set_list = cmdb.get_sets_info(username, bk_biz_id=business["bk_biz_id"])["data"]["info"]
    online_set_dict = {}
    for sett in set_list:
        db_sett = {
            "bk_biz_id": business["bk_biz_id"],
            "bk_set_id": sett["bk_set_id"],
            "bk_set_name": sett["bk_set_name"],
        }
        online_set_dict[sett["bk_set_id"]] = Set(**db_sett)

    bulk_create_or_update_delete(
        Set,
        primary_key_name="bk_set_id",
        bk_biz_id=business["bk_biz_id"],
        online_data_dict=online_set_dict,
        fields=["bk_set_name", "bk_biz_id"],
    )

    # 保存模块信息到模块表
    module_list = cmdb.get_modules_info(username, bk_biz_id=business["bk_biz_id"])["data"]["info"]
    online_module_dict = {}
    for module in module_list:
        db_module = {
            "bk_biz_id": business["bk_biz_id"],
            "bk_set_id": module["bk_set_id"],
            "bk_module_id": module["bk_module_id"],
            "bk_module_name": module["bk_module_name"],
        }
        online_module_dict[module["bk_module_id"]] = Module(**db_module)

    bulk_create_or_update_delete(
        Module,
        primary_key_name="bk_module_id",
        bk_biz_id=business["bk_biz_id"],
        online_data_dict=online_module_dict,
        fields=["bk_module_name", "bk_biz_id", "bk_set_id"],
    )

    # 保存主机信息到主机信息表
    host_list = get_page_data(username, cmdb.get_host_info, business["bk_biz_id"], PageDataLimit.HOST_PAGE_LIMIT)
    online_host_dict = {}
    for host in host_list:
        db_host = {
            "bk_host_id": host["bk_host_id"],
            "bk_host_name": host["bk_host_name"],
            "bk_host_innerip": host["bk_host_innerip"],
            "bk_host_outerip": host["bk_host_outerip"],
            "host_system": host["host_system"],
            "operator": host["operator"],
            "bk_bak_operator": host["bk_bak_operator"],
            "bk_cloud_id": host["bk_cloud_id"],
            "bk_cloud_name": host["bk_cloud_name"],
            "bk_biz_id": business["bk_biz_id"],
            "bk_set_id": host["bk_set_id"],
            "bk_module_id": host["bk_module_id"]
        }
        online_host_dict[host["bk_host_id"]] = Host(**db_host)

    bulk_create_or_update_delete(
        Host,
        primary_key_name="bk_host_id",
        bk_biz_id=business["bk_biz_id"],
        online_data_dict=online_host_dict,
        fields=["bk_host_innerip", "bk_host_name", "bk_host_outerip", "operator", "bk_bak_operator", "bk_cloud_id",
                "bk_cloud_name", "host_system", "bk_biz_id", "bk_set_id", "bk_module_id"],
    )

    if is_finished:
        cache.set("sync_all", SyncTaskStatus.IDLE, timeout=1800)


@task()
def backup_host_files_task(username, data):
    """
    备份主机文件
    """
    file_directory = data["file_directory"]
    file_list = data["file_list"]

    file_abs_list = [posixpath.join(file_directory, file_name) for file_name in file_list]
    file_abs_str = ",".join(file_abs_list)
    params = f"wheel-w_backup_directory {file_abs_str} '{data['file_suffix']}'"
    result, script_logs, params = job.execute_script_get_log(username, "backup_host_files", data, params)
    if not result:
        logger.info(f"备份文件脚本执行失败 params:{params} script_logs:{script_logs}")
        return
    ip_list = params["ip_list"]
    kwargs = {
        "bk_biz_id": params["bk_biz_id"],
        "job_instance_id": params["job_instance_id"],
        "backup_operator": params["username"],
    }
    backup_record_list = []
    for ip in ip_list:
        cur_log = script_logs[ip["ip"]].split("\n")
        kwargs["bk_host_innerip"] = ip["ip"]
        kwargs["backup_directory"] = cur_log[1]
        kwargs["file_suffix"] = cur_log[2]
        kwargs["backup_file_name"] = cur_log[3]
        backup_record_list.append(BackupHostFileRecord(**kwargs))

    BackupHostFileRecord.objects.bulk_create(backup_record_list)


@task()
def search_host_files_task(username, data):
    """
    搜索主机文件
    """
    ip_list = data["ip_list"]
    file_path = data["file_path"]
    result, script_logs, _ = job.execute_script_get_log(
        username, "search_host_files", data, f"{file_path} {data['file_suffix']}"
    )
    if not result:
        cache.set(search_host_files_task.request.id, {"message": script_logs}, timeout=300)
        logger.info(f"搜索文件脚本执行失败 params:{file_path} {data['file_suffix']} script_logs:{script_logs}")
        return

    result = {"file_list": [], "fail_host_info": []}
    for ip in ip_list:
        log_content = script_logs[ip["ip"]]
        if "job_success" in log_content:
            cur_ip_file_list = log_content.split("\n")[1:-2]
            cur_ip_file_size = int(cur_ip_file_list.pop())
            result["file_list"].append(
                {
                    "ip": ip,
                    "bk_cloud_id": ip["bk_cloud_id"],
                    "file_list": ",".join(cur_ip_file_list),
                    "file_size": cur_ip_file_size,
                    "file_count": len(cur_ip_file_list),
                    "file_directory": file_path,
                }
            )
        else:
            result["fail_host_info"].append({"ip": ip["ip"], "err_msg": log_content})

    cache.set(search_host_files_task.request.id, result, timeout=300)

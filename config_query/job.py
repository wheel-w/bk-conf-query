# -*- coding: utf-8 -*-
import time

from blueking.component.shortcuts import get_client_by_user

from config_query.base import JobExecuteStatus, ScriptLanguage
from config_query.job_scripts.base import get_script_base64


def execute_script_get_log(username, script_name, data, params, timeout=300):
    """
    执行脚本并获取返回值
    """
    bk_biz_id = data["bk_biz_id"]
    ip_list = data["ip_list"]
    kwargs = {
        "username": username,
        "script_name": script_name,
        "bk_biz_id": bk_biz_id,
        "params": params,
        "ip_list": ip_list,
    }
    response = fast_execute_script(**kwargs)
    if not response["result"]:
        return False, response["message"], None

    job_instance_id = response["data"]["job_instance_id"]
    step_instance_id = response["data"]["step_instance_id"]
    request_count = 0
    while True:
        execute_status_result = get_job_instance_status(username, bk_biz_id, job_instance_id)
        request_count += 1
        if (
            execute_status_result["data"]["job_instance"]["status"]
            in (JobExecuteStatus.SUCCESS, JobExecuteStatus.FAILED)
            or request_count > timeout
        ):
            break
        time.sleep(1)

    kwargs = {
        "username": username,
        "bk_biz_id": bk_biz_id,
        "job_instance_id": job_instance_id,
        "step_instance_id": step_instance_id,
    }
    script_logs = {}
    for ip in ip_list:
        kwargs["bk_cloud_id"] = ip["bk_cloud_id"]
        kwargs["ip"] = ip["ip"]
        log_content = get_job_instance_ip_log(**kwargs)["data"]["log_content"]
        script_logs[ip["ip"]] = log_content

    return (
        True,
        script_logs,
        {"bk_biz_id": bk_biz_id, "job_instance_id": job_instance_id, "ip_list": ip_list, "username": username},
    )


def fast_execute_script(username, script_name=None, bk_biz_id=None, params=None, ip_list=None):
    """
    快速执行脚本
    """
    client = get_client_by_user(user=username)
    script_content, script_param = get_script_base64(script_name, params)
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "script_content": script_content,
        "script_param": script_param,
        "script_language": ScriptLanguage.PYTHON,
        "account_alias": "root",
        "target_server": {"ip_list": ip_list},
    }

    result = client.jobv3.fast_execute_script(kwargs)
    return result


def get_job_instance_status(username, bk_biz_id=None, job_instance_id=None):
    """
    根据作业实例 ID 查询作业执行状态
    """
    client = get_client_by_user(user=username)

    kwargs = {"bk_biz_id": bk_biz_id, "job_instance_id": job_instance_id}
    result = client.jobv3.get_job_instance_status(kwargs)

    return result


def get_job_instance_ip_log(
    username, bk_biz_id=None, bk_cloud_id=None, job_instance_id=None, step_instance_id=None, ip=None
):
    """
    根据作业实例ID查询作业执行日志
    """
    client = get_client_by_user(user=username)
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "job_instance_id": job_instance_id,
        "step_instance_id": step_instance_id,
        "bk_cloud_id": bk_cloud_id,
        "ip": ip,
    }
    result = client.jobv3.get_job_instance_ip_log(kwargs)

    return result

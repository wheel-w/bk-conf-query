# -*- coding: utf-8 -*-
import logging
import os
import requests

from config_query.base import HTTP_GET

CMDB_API_HOST = os.getenv("CMDB_API_HOST", "")

logger = logging.getLogger("root")


def _request_cmdb_api(api_name, request_method, query_params={}):
    url = "{}/{}".format(CMDB_API_HOST, api_name)
    try:
        text = ""
        response = requests.request(request_method, url, params=query_params)
        text = response.text

        response.raise_for_status()
        data = response.json()
        result = {
            "result": True,
            "data": {
                "count": data["count"],
                "info": data["results"]
            }
        }
    except Exception as e:
        logger.exception(e)
        result = {
            "result": False,
            "data": {},
            "message": text or str(e)
        }

    return result


def get_business_info(username):
    """
    获取cmdb所有业务信息
    """

    result = _request_cmdb_api("api/business_list/", HTTP_GET)

    return result


def get_sets_info(username, bk_biz_id):
    """
    获取当前业务下集群信息
    """
    query_params = {
        "bk_biz_id": bk_biz_id
    }
    result = _request_cmdb_api("api/set_list/", HTTP_GET, query_params)

    return result


def get_modules_info(username, bk_biz_id):
    """
    获取当前集群下的所有模块
    """
    query_params = {
        "bk_biz_id": bk_biz_id
    }
    result = _request_cmdb_api("api/module_list/", HTTP_GET, query_params)

    return result


def get_host_info(username, params):
    """
    获取主机信息
    """
    query_params = {
        "bk_biz_id": params["bk_biz_id"],
        "page": params["page"],
        "page_size": params["page_size"]
    }
    result = _request_cmdb_api("api/host_list/", HTTP_GET, query_params)

    return result


def get_host_base_info(username, bk_host_id=None):
    """
    获取主机详细信息
    """
    query_params = {
        "bk_host_id": bk_host_id
    }
    result = _request_cmdb_api("api/host_list/", HTTP_GET, query_params)

    return result

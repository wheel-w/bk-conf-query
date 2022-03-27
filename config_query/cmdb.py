# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_user


def get_business_info(username):
    """
    获取cmdb所有业务信息
    """
    client = get_client_by_user(user=username)

    kwargs = {"fields": ["bk_biz_id", "bk_biz_name"]}

    response = client.cc.search_business(kwargs)

    return response


def get_sets_info(username, bk_biz_id):
    """
    获取当前业务下集群信息
    """
    client = get_client_by_user(user=username)

    kwargs = {"bk_biz_id": bk_biz_id, "fields": ["bk_set_name", "bk_set_id"]}

    response = client.cc.search_set(kwargs)

    return response


def get_modules_info(username, bk_biz_id=None, bk_set_id=None):
    """
    获取当前集群下的所有模块
    """
    client = get_client_by_user(user=username)

    if bk_set_id:
        kwargs = {"bk_biz_id": bk_biz_id, "bk_set_id": bk_set_id, "fields": ["bk_module_name", "bk_module_id"]}
    else:
        kwargs = {"bk_biz_id": bk_biz_id, "fields": ["bk_module_name", "bk_module_id", "bk_set_id"]}

    response = client.cc.search_module(kwargs)

    return response


def get_host_info(username, params):
    """
    获取主机信息
    """
    client = get_client_by_user(user=username)
    kwargs = {
        "bk_biz_id": int(params["bk_biz_id"]),
        "fields": [
            "bk_host_innerip",
            "bk_host_id",
            "bk_host_name",
            "bk_host_outerip",
            "operator",
            "bk_bak_operator",
            "bk_cloud_id",
        ],
        "page": {"start": int(params["start"]), "limit": int(params["limit"])},
    }
    if "bk_set_id" in params:
        kwargs["bk_set_ids"] = [
            int(params["bk_set_id"]),
        ]

    if "bk_module_id" in params:
        kwargs["bk_module_ids"] = [
            int(params["bk_module_id"]),
        ]

    response = client.cc.list_biz_hosts(kwargs)

    return response


def get_business_topo(username, params):
    """
    获取业务拓扑
    """
    client = get_client_by_user(user=username)

    kwargs = {"bk_biz_id": params["bk_biz_id"], "page": {"start": int(params["start"]), "limit": int(params["limit"])}}

    response = client.cc.find_host_topo_relation(kwargs)

    return response


def search_host_list(username, params):
    client = get_client_by_user(user=username)

    kwargs = {
        "fields": [
            "bk_host_id",
            "bk_host_name",
            "bk_host_innerip",
            "bk_host_outerip",
            "bk_cloud_id",
            "operator",
            "bk_bak_operator",
        ],
        "page": {"start": params["start"], "limit": params["limit"]},
    }
    if "bk_biz_id" in params:
        kwargs["bk_biz_id"] = params["bk_biz_id"]

    if "bk_set_id" in params:
        kwargs["bk_set_ids"] = [
            params["bk_set_id"],
        ]

    if "bk_module_id" in params:
        kwargs["bk_module_ids"] = [
            params["bk_module_id"],
        ]

    host_property_filter = {"condition": "AND", "rules": []}

    fields = [
        {"field": "bk_host_id", "operator": "equal"},
        {"field": "bk_cloud_id", "operator": "equal"},
        {"field": "operator", "operator": "contains"},
        {"field": "bk_host_name", "operator": "contains"},
        {"field": "bk_bak_operator", "operator": "contains"},
        {"field": "bk_bak_operator", "operator": "contains"},
        {"field": "bk_host_innerip", "operator": "begins_with"},
        {"field": "bk_host_outerip", "operator": "begins_with"},
    ]

    for field in fields:
        if field["field"] in params:
            field["value"] = params[field["field"]]
            host_property_filter["rules"].append(field)

    if host_property_filter["rules"]:
        kwargs["host_property_filter"] = host_property_filter

    if "bk_biz_id" in kwargs:
        response = client.cc.list_biz_hosts(kwargs)
    else:
        response = client.cc.list_hosts_without_biz(kwargs)

    return response


def get_host_base_info(username, bk_host_id=None):
    """
    获取主机详细信息
    """
    client = get_client_by_user(user=username)

    kwargs = {
        "bk_host_id": bk_host_id,
    }

    response = client.cc.get_host_base_info(kwargs)

    return response

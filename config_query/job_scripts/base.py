# -*- coding: utf-8 -*-
import base64

SCRIPT_SETS = {
    "search_host_files": "config_query/job_scripts/search_host_files",
    "backup_host_files": "config_query/job_scripts/backup_host_files",
}


def get_script_base64(script_name, params=""):
    """
    获取对应脚本的base64编码
    """
    with open(SCRIPT_SETS[script_name], "r", encoding="utf-8") as f:
        script_content = f.read()

    return base64.b64encode(script_content.encode("utf8")).decode("utf-8"), base64.b64encode(
        params.encode("utf8")
    ).decode("utf-8")

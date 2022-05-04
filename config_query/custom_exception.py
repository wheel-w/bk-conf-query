# -*- coding: utf-8 -*-
from rest_framework.views import exception_handler  # 继承默认exception_handler

from config_query.response import ConfigQueryResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # 重新定义

    if hasattr(context["view"], "status") and context["view"].status == 403:
        response = ConfigQueryResponse(data=context["view"].permission_url, code=403)

    return response

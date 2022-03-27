# -*- coding: utf-8 -*-
from rest_framework.pagination import LimitOffsetPagination


class ConfigQueryLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "start"
    max_limit = 100

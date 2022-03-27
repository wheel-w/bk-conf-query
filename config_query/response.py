# -*- coding: utf-8 -*-
from django.utils import six
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class ConfigQueryResponse(Response):
    """An HttpResponse that allows its data to be rendered into arbitrary media types."""

    def __init__(
        self,
        data=None,
        code=0,
        request_id=None,
        message="success",
        result=True,
        status=None,
        count=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                "You passed a Serializer instance as data, but "
                "probably meant to pass serialized `.data` or "
                "`.error`. representation."
            )
            raise AssertionError(msg)

        self.data = {"code": code, "message": message, "result": result, "request_id": request_id, "data": data}
        if count:
            self.data["count"] = count
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value

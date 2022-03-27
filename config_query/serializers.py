# -*- coding: utf-8 -*-
from rest_framework import serializers

from config_query.models import BackupHostFileRecord, Business, Host, Module, Set


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = "__all__"


class BackupHostFileRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupHostFileRecord
        fields = "__all__"


class HostIpSerializer(serializers.Serializer):
    """
    主机IP序列化
    """

    ip = serializers.IPAddressField()
    bk_cloud_id = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class JobSearchHostSerializer(serializers.Serializer):
    """
    查询主机文件参数校验
    """

    file_path = serializers.CharField()
    file_suffix = serializers.CharField()
    bk_biz_id = serializers.IntegerField()
    ip_list = HostIpSerializer(many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class JobBackupHostSerializer(serializers.Serializer):
    """
    备份主机文件参数校验
    """

    file_directory = serializers.CharField()
    file_suffix = serializers.CharField()
    bk_biz_id = serializers.IntegerField()
    ip_list = HostIpSerializer(many=True)
    file_list = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

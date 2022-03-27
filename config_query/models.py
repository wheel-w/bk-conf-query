# -*- coding: utf-8 -*-
from blueapps.utils import get_request
from django.db import models


# Create your models here.
class Business(models.Model):
    """
    业务表
    """

    bk_biz_id = models.IntegerField(verbose_name="业务ID", primary_key=True)
    bk_biz_name = models.CharField(verbose_name="业务名称", max_length=128)

    class Meta:
        verbose_name = "业务信息表"
        verbose_name_plural = verbose_name
        db_table = "config_query_business"

        def __str__(self):
            return self.bk_biz_name


class Set(models.Model):
    """
    集群信息表
    """

    bk_set_id = models.IntegerField(verbose_name="集群ID", primary_key=True)
    bk_set_name = models.CharField(verbose_name="集群名称", max_length=128)
    bk_biz_id = models.IntegerField(verbose_name="所属业务ID")

    class Meta:
        verbose_name = "集群信息表"

        verbose_name_plural = verbose_name
        db_table = "config_query_set"

    def __str__(self):
        return self.bk_set_name


class Module(models.Model):
    """
    模块信息表
    """

    bk_module_id = models.IntegerField(verbose_name="模块ID", primary_key=True)
    bk_module_name = models.CharField(verbose_name="模块名称", max_length=100)
    bk_set_id = models.IntegerField(verbose_name="所属集群ID", blank=True, null=True)
    bk_biz_id = models.IntegerField(verbose_name="所属业务ID")

    class Meta:
        verbose_name = "模块信息表"
        verbose_name_plural = verbose_name
        db_table = "config_query_module"

    def __str__(self):
        return self.bk_module_name


class Host(models.Model):
    """
    主机信息表
    """

    bk_host_id = models.IntegerField(verbose_name="主机ID", primary_key=True)
    bk_host_name = models.CharField(verbose_name="主机名称", max_length=128, blank=True, null=True)
    bk_host_innerip = models.CharField(verbose_name="内网IP", max_length=128, blank=True, null=True)
    bk_host_outerip = models.CharField(verbose_name="外网IP", max_length=128, blank=True, null=True)
    host_system = models.CharField(verbose_name="操作系统类型", max_length=128, blank=True, null=True)
    operator = models.TextField(verbose_name="负责人", blank=True, null=True)
    bk_bak_operator = models.TextField(verbose_name="备份负责人", blank=True, null=True)
    bk_cloud_id = models.IntegerField(verbose_name="云区域", blank=True, null=True)
    bk_cloud_name = models.CharField(verbose_name="云区域名称", max_length=128, blank=True, null=True)
    bk_biz_id = models.CharField(verbose_name="所属业务ID", max_length=128, default="")
    bk_set_id = models.CharField(verbose_name="所属集群ID", max_length=128, default="")
    bk_module_id = models.CharField(verbose_name="所属模块ID", max_length=128, default="")

    class Meta:
        verbose_name = "主机信息表"
        verbose_name_plural = verbose_name
        db_table = "config_query_host"

    def __str__(self):
        return self.bk_host_id


class BackupHostFileRecord(models.Model):
    """
    备份主机文件备份表
    """

    bk_biz_id = models.IntegerField(verbose_name="业务ID")
    job_instance_id = models.BigIntegerField(verbose_name="作业实例ID")
    bk_host_innerip = models.CharField(verbose_name="主机IP", max_length=128)
    backup_directory = models.CharField(verbose_name="文件目录", max_length=256)
    file_suffix = models.CharField(verbose_name="文件后缀", max_length=32)
    backup_file_name = models.CharField(verbose_name="备份文件名", max_length=256)
    backup_time = models.DateTimeField(verbose_name="备份时间", auto_now_add=True)
    backup_operator = models.CharField(verbose_name="备份人", max_length=256)

    def __str__(self):
        return self.bk_host_innerip

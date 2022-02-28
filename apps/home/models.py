# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Doingame(models.Model):
    ten = models.CharField(max_length=255)
    gia_tien_xu = models.FloatField()
    gia_tien_atm = models.FloatField()
    so_luong = models.FloatField()
    trang_thai = models.SmallIntegerField(default=1)
    thong_tin = models.CharField(max_length=255)
    sap_xep = models.IntegerField(default=0)

    class Meta:
        ordering = ('-sap_xep',)


class TaiKhoan(models.Model):
    thong_tin = models.CharField(max_length=255)
    gia_tien_xu = models.FloatField()
    gia_tien_atm = models.FloatField()
    soluong = models.FloatField()
    trang_thai = models.SmallIntegerField(default=1)


class DichVuGame(models.Model):
    ten = models.CharField(max_length=255)
    gia_tien_xu = models.FloatField()
    gia_tien_atm = models.FloatField()
    trang_thai = models.SmallIntegerField(default=1)
    thong_tin = models.CharField(max_length=255)


class GiaoDich(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    ma_hoa_don = models.IntegerField()
    so_luong = models.IntegerField(default=0)
    ngay_gio_giao_dich = models.DateTimeField(auto_now=True)
    thong_tin = models.CharField(max_length=255, null=True)

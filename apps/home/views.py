# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import random

from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse

# @login_required(login_url="/login/")
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from apps.home.models import Doingame, DichVuGame, TaiKhoan, GiaoDich


def index(request):
    query_set = Doingame.objects.all()
    context = {
        'segment': 'index',
        'doingame': list(query_set.values()),
        'dichvugame': list(DichVuGame.objects.all()),
        'taikhoan': list(TaiKhoan.objects.all()),
        'tongtruycap': random.randint(10000, 20000),
        'nguoidungmoi': random.randint(500, 1000),
        'daban': random.randint(500, 1000)
    }
    print(context['doingame'])
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@csrf_exempt
@transaction.atomic
def muahang(request):
    magiaodich = ''
    thongtin = request.POST.get('thongtin')
    soluong = request.POST.get('soluong')
    if not thongtin or int(soluong) <= 0:
        message_txt = "Bạn chưa chọn thông tin hoặc số lượng !!"
        context = {
            'magiaodich': magiaodich,
            'message_txt': message_txt
        }

        return JsonResponse(context)

    if int(soluong) >= 99999:
        message_txt = "Số lượng tối đa là: 99999 !!"
        context = {
            'magiaodich': magiaodich,
            'message_txt': message_txt
        }

        return JsonResponse(context)
    try:
        magiaodich = random.randint(0, 10000000)
        GiaoDich(ma_hoa_don=magiaodich, thong_tin=thongtin, so_luong=soluong).save()
        dg = Doingame.objects.get(ten__contains=thongtin)
        a = dg.so_luong - int(soluong)
        dg.so_luong = a
        dg.save()
        message_txt = f'Bạn đã mua {soluong} {thongtin} !. Mã giao dịch của bạn là:{magiaodich}. ' \
                      'Vui lòng đến khu 86 làng Toge inbox mã giao dịch để nhận đồ!'
    except Exception:
        message_txt = 'Mua hàng thất bại do hết sản phẩm !. Vui lòng thử lại sau'
        context = {
            'magiaodich': magiaodich,
            'message_txt': message_txt
        }
        return JsonResponse(context)

    context = {
        'magiaodich': magiaodich,
        'message_txt': message_txt
    }
    return JsonResponse(context)

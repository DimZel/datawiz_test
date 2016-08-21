# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from dwapi import datawiz
import datetime
import stats
from django.contrib import auth
from login.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def main(request):
    user = auth.get_user(request)
    username = user.get_username()
    if not username:
        return redirect('login')
    try:
        user_profile = UserProfile.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        return redirect('login')
    secret = user_profile.secret

    dw = datawiz.DW(username, secret)
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    if date_from:
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    if date_to:
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    data = get_data(dw, date_from, date_to)
    date_from, date_to, client, statistics, increase, decrease = data
    context = {'statistics': statistics,
               'increase': increase,
               'decrease': decrease,
               'date_from': date_from,
               'date_to': date_to,
               'client': client}
    return render(request, 'base.html', context)


def refresh(request):
    user = auth.get_user(request)
    username = user.get_username()
    user_profile = UserProfile.objects.get(user_id=user.id)
    secret = user_profile.secret

    dw = datawiz.DW(username, secret)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    data = get_data(dw, date_from, date_to)
    date_from, date_to, _, statistics, increase, decrease = data
    context = {'statistics': statistics,
               'increase': increase,
               'decrease': decrease,
               'date_from': date_from,
               'date_to': date_to}
    return render(request, 'data.html', context)


def get_data(dw, date_from, date_to):
    statistic = stats.Statistics(dw, date_from, date_to)
    client = statistic.client
    date_from = statistic.date_from
    date_to = statistic.date_to
    statistic.receive_data()
    statistics_df = statistic.get_statistics()
    statistics_df['indicators'] = ['Оборот', 'Количество товаров', 'Количество чеков', 'Средний чек']

    statistic.calc_difference()
    increase_products = statistic.get_increase_products()
    decrease_products = statistic.get_decrease_products()

    statistics_table = statistics_df.to_html(
        classes='table table-bordered table-hover table-sm', index=False, header=False)
    increase_table = increase_products.to_html(
        classes='table table-bordered table-hover table-sm', index=False, header=False)
    decrease_table = decrease_products.to_html(
        classes='table table-bordered table-hover table-sm', index=False, header=False)
    return (date_from, date_to, client, statistics_table, increase_table, decrease_table)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from models import Bank, User, Trans


class BankView(generic.ListView):
    template_name = 'bank.html'
    context_object_name = 'banks'

    def get_queryset(self):
        return Bank.objects.filter(is_central='0')


class BankCreate(CreateView):
    model = Bank
    fields = ['name', 'balance', 'is_central']


class BankUpdate(UpdateView):
    model = Bank
    fields = ['name', 'balance', 'is_central']


class BankDelete(DeleteView):
    model = Bank
    success_url = reverse_lazy('banks')


class OfficerView(generic.ListView):
    template_name = 'officer.html'
    context_object_name = 'officers'

    def get_queryset(self):
        login_required()
        return User.objects.all()


class OfficerCreate(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'user_type', 'bank']


class OfficerUpdate(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'user_type', 'bank']


class OfficerDelete(DeleteView):
    model = User
    success_url = reverse_lazy('officers')


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def trans(request):
    bank = Bank.objects.get(pk=request.user.bank_id)
    trans = bank.trans_set.all()
    dict = {
        'trans': trans,
        'bank': bank
    }
    return render(request, 'trans.html', context=dict)


@login_required
def trans_add(request):
    if request.method == 'POST':
        tran = Trans()
        tran.type = request.POST['type']
        tran.amount = request.POST['amount']
        tran.date = datetime.datetime.now()
        tran.bank = Bank.objects.get(pk=request.user.bank_id)
        tran.officer = User.objects.get(pk=request.user.id)

        bank = Bank.objects.get(pk=request.user.bank_id)
        if tran.type == 'D':
            bank.balance = int(bank.balance) + int(tran.amount)
        elif tran.type == 'C':
            bank.balance = int(bank.balance) - int(tran.amount)

        bank.save()
        tran.save()
        return redirect('/transactions/')
    elif request.method == 'GET':
        return render(request, 'trans-add.html')


@login_required
def monitor(request):
    banks = Bank.objects.filter(is_central=0)
    trans = Trans.objects.all()
    return render(request, 'monitor.html', {'banks': banks, 'trans': trans})

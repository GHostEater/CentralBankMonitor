# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from models import Bank, User, Trans, SpecialTrans, BankOfficer, CentralOfficer
from forms import BankOfficerForm, SpecialTransRequestForm, SpecialTransProcessForm, ReportForm


class BankView(generic.ListView):
    template_name = 'bank.html'
    context_object_name = 'banks'

    def get_queryset(self):
        return Bank.objects.all()


class BankCreate(CreateView):
    model = Bank
    fields = ['name', 'balance', 'type']


class BankUpdate(UpdateView):
    model = Bank
    fields = ['name', 'balance', 'type']


class BankDelete(DeleteView):
    model = Bank
    success_url = reverse_lazy('banks')


class OfficerCreate(CreateView):
    model = BankOfficer
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'type', 'bank']


class OfficerUpdate(UpdateView):
    model = BankOfficer
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'type', 'bank']


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def bank_officer(request):
    officer = BankOfficer.objects.all()
    dict = {'officers': officer}
    return render(request, 'bank-officer.html', context=dict)


@login_required
def bank_officer_create(request):
    form = BankOfficerForm()
    if request.method == 'POST':
        form = BankOfficerForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.username
            user.password = form.password
            user.first_name = form.first_name
            user.last_name = form.last_name
            user.email = form.email
            user.type = 3
            user.save()

            officer = BankOfficer()
            officer.user = user
            officer.bank = form.bank
            officer.save()
        return redirect('/bank-officers/')
    else:
        return render(request, 'bank-officer-create.html', context={'form': form})


@login_required
def bank_officer_edit(request, id):
    bank_officer = BankOfficer.objects.get(pk=id)
    data = {
        'username': bank_officer.user.username,
        'first_name': bank_officer.user.first_name,
        'last_name': bank_officer.user.last_name,
        'email': bank_officer.user.email,
        'bank': bank_officer.bank.id
    }
    form = BankOfficerForm(initial=data)
    if request.method == 'POST':
        form = BankOfficerForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=bank_officer.user.id)
            user.username = form.username
            user.password = form.password
            user.first_name = form.first_name
            user.last_name = form.last_name
            user.email = form.email
            user.type = 3
            user.save()

            officer = BankOfficer.objects.get(pk=bank_officer.id)
            officer.user = user
            officer.bank = form.bank
            officer.save()
        return redirect('/bank-officers/')
    else:
        return render(request, 'bank-officer-create.html', context={'form': form})


class BankOfficerDelete(DeleteView):
    model = BankOfficer
    success_url = reverse_lazy('bank-officers')


@login_required
def spec_trans(request):
    if request.user.type == 3:
        bank = Bank.objects.get(pk=request.user.bank_id)
        trans = bank.specialtrans_set.all()
        dict = {
            'trans': trans,
            'bank': bank
        }
    elif request.user.type == 2:
        trans = SpecialTrans.objects.filter(status=0)
        dict = {'trans': trans}
    else:
        dict = {}
    return render(request, 'spec-trans.html', context=dict)


def spec_trans_report(request):
    form = ReportForm()
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.type == 1:
            trans = SpecialTrans.objects.filter(date__month=form.month, status=1)
        elif form.type == 2:
            trans = SpecialTrans.objects.filter(date__year=form.year, status=1)
        dict = {
            'trans': trans,
            'form': form
        }
        return render(request, 'spec-trans-report.html', context=dict)
    else:
        return render(request, 'spec-trans-report.html', context={'form': form})


@login_required
def spec_trans_request(request):
    form = SpecialTransRequestForm()
    if request.method == 'POST':
        form = SpecialTransRequestForm(request.POST)
        if form.is_valid():
            bank_officer = BankOfficer.objects.get(user=request.user.id)
            tran = form.save(commit=False)
            tran.bank_officer = request.user.id
            tran.bank = bank_officer.bank.id
            tran.save()
        return redirect('/special-transactions/')
    else:
        return render(request, 'spec-trans-request.html', context={'form': form})


@login_required
def spec_trans_process(request, id):
    form = SpecialTransProcessForm()
    if request.method == 'POST':
        form = SpecialTransProcessForm(request.POST)
        if form.is_valid():
            tran = SpecialTrans.objects.get(pk=id)
            tran.status = form.status
            tran.reason = form.reason
            tran.date = datetime.datetime.now()
            tran.central_officer = request.user.id
        return redirect('/special-transactions/')
    else:
        return render(request, 'spec-trans-process.html', context={'form': form})


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
def trans_report(request):
    form = ReportForm()
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.type == 1:
            trans = Trans.objects.filter(date__month=form.month, status=1)
        elif form.type == 2:
            trans = Trans.objects.filter(date__year=form.year, status=1)
        dict = {
            'trans': trans,
            'form': form
        }
        return render(request, 'trans-report.html', context=dict)
    else:
        return render(request, 'trans-report.html', context={'form': form})


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
        if tran.type == 'Debit':
            bank.balance = int(bank.balance) + int(tran.amount)
        elif tran.type == 'Credit':
            bank.balance = int(bank.balance) - int(tran.amount)

        bank.save()
        tran.save()
        return redirect('/transactions/')
    elif request.method == 'GET':
        return render(request, 'trans-add.html')


@login_required
def monitor(request):
    banks = Bank.objects.objects.all()
    trans = Trans.objects.all()
    return render(request, 'monitor.html', {'banks': banks, 'trans': trans})

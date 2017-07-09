# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


# Create your models here.


class Bank(models.Model):
    type_choices = (
        ('Commercial', 'Commercial'),
        ('Micro-finance', 'Micro-finance'),
    )
    name = models.CharField(max_length=200)
    balance = models.FloatField(default=0, verbose_name='Capital Adequacy')
    type = models.CharField(max_length=20, choices=type_choices)
    limit = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('banks')

    def __str__(self):
        return str(self.name) + " " + str(self.balance)


@receiver(pre_save, sender='bankMonitor.Bank')
def callback(sender, instance, *args, **kwargs):
    if instance.type == 'Commercial':
        instance.limit = 25000000000
    elif instance.type == 'Micro-finance':
        instance.limit = 10000000000


class User(AbstractUser):
    type_choices = (
        (1, 'Super User'),
        (2, 'Central Officer'),
        (3, 'Bank Officer'),
    )
    type = models.IntegerField(choices=type_choices, default=3)

    def get_absolute_url(self):
        return reverse('officers')


@receiver(pre_save, sender='bankMonitor.User')
def my_callback(sender, instance, *args, **kwargs):
    new_password = instance.password
    try:
        old_password = User.objects.get(pk=instance.pk).password
    except User.DoesNotExist:
        old_password = None
    if new_password != old_password:
        instance.password = make_password(instance.password)


class CentralOfficer(models.Model):
    user = models.OneToOneField(User)


class BankOfficer(models.Model):
    user = models.OneToOneField(User)
    bank = models.ForeignKey(Bank, null=True, blank=True)


def create_profile(sender, **kwargs):
    if kwargs['instance'].type == 2:
        if CentralOfficer.objects.get(user=kwargs['instance']).DoesNotExist():
            acad = CentralOfficer.objects.create(user=kwargs['instance'])
    if kwargs['instance'].type == 3:
        if BankOfficer.objects.get(user=kwargs['instance']).DoesNotExist():
            acad = BankOfficer.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class Trans(models.Model):
    type_choices = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )
    type = models.CharField(max_length=10, choices=type_choices, default='Debit')
    amount = models.IntegerField(default=0)
    bank_officer = models.ForeignKey(User)
    bank = models.ForeignKey(Bank)
    date = models.DateTimeField(default='')


class SpecialTrans(models.Model):
    type_choices = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )
    trans_type_choices = (
        ('Loan', 'Loan'),
        ('Risk Asset', 'Risk Asset'),
        ('Investment', 'Investment'),
    )
    detail = models.TextField(default='')
    reason = models.TextField(default='', null=True, blank=True)
    type = models.CharField(max_length=10, choices=type_choices)
    trans_type = models.CharField(max_length=15, choices=trans_type_choices)
    amount = models.IntegerField(default=0)
    bank_officer = models.ForeignKey(User, related_name='bank_officer')
    bank = models.ForeignKey(Bank)
    status = models.IntegerField(default=0)
    central_officer = models.ForeignKey(User, related_name='central_officer', null=True, blank=True)
    date = models.DateTimeField(default='')

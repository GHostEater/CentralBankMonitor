# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


# Create your models here.


class Bank(models.Model):
    name = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)
    is_central = models.BooleanField(default=0)

    def get_absolute_url(self):
        return reverse('banks')

    def __str__(self):
        return str(self.name) + " " + str(self.balance)


class User(AbstractUser):
    type_choices = (
        ('SU', 'Super User'),
        ('A', 'Central Officer'),
        ('B', 'Bank Officer'),
    )
    user_type = models.CharField(max_length=2, choices=type_choices, default='B')
    bank = models.ForeignKey(Bank, default=0)

    def get_absolute_url(self):
        return reverse('officers')


@receiver(pre_save, sender='bankMonitor.User')
def my_callback(sender, instance, *args, **kwargs):
    instance.password = make_password(instance.password)


class Trans(models.Model):
    type_choices = (
        ('D', 'Debit'),
        ('C', 'Credit'),
    )
    type = models.CharField(max_length=2, choices=type_choices, default='D')
    amount = models.IntegerField(default=0)
    officer = models.ForeignKey(User)
    bank = models.ForeignKey(Bank)
    date = models.DateTimeField(default='')

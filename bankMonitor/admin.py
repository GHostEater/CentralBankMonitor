# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from bankMonitor.models import Bank, User, Trans, BankOfficer, CentralOfficer, SpecialTrans

# Register your models here.
admin.site.register(Bank)
admin.site.register(User)
admin.site.register(Trans)
admin.site.register(BankOfficer)
admin.site.register(CentralOfficer)
admin.site.register(SpecialTrans)

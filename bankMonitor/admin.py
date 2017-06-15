# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from bankMonitor.models import Bank, User, Trans

# Register your models here.
admin.site.register(Bank)
admin.site.register(User)
admin.site.register(Trans)

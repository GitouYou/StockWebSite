# -*- coding: utf-8 -*-
from django.contrib import admin
from finweb.models import UserProfile,Portfolio,Stockdata
from django.contrib.auth.models import User
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','gender','phonenum','birthday','list')

admin.site.register(UserProfile,ProfileAdmin)
admin.site.register(Portfolio)
admin.site.register(Stockdata)

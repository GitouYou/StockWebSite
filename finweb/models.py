# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    #UserProfile模型，和已有的User模型一起使用
    # username = models.CharField(max_length=30,unique=True)
    # password = models.CharField(max_length=20)
    # email = models.EmailField(max_length=50,unique=True)
    MAN = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MAN, '男'),
        (FEMALE, '女'),
    )
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=5,choices= GENDER_CHOICES,default= MAN)
    phonenum = models.CharField(max_length=15)
    birthday = models.DateField()
    #默认值为空
    list = models.TextField(blank=True)
    def __unicode__(self):
        return self.user.username

class Portfolio(models.Model):
    #此处的User可能改动
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    #默认值为空
    list = models.TextField(blank=True)
    def __unicode__(self):
        #不一定正确
        return self.user.username + ':'+self.name


class Stockdata(models.Model):
    index = models.BigIntegerField(blank=True,primary_key=True)
    code = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True)
    industry = models.TextField(blank=True)
    area = models.TextField(blank=True)
    pe = models.FloatField(blank=True, null=True)
    outstanding = models.FloatField(blank=True, null=True)
    totals = models.FloatField(blank=True, null=True)
    totalassets = models.FloatField(db_column='totalAssets', blank=True, null=True)  # Field name made lowercase.
    liquidassets = models.FloatField(db_column='liquidAssets', blank=True, null=True)  # Field name made lowercase.
    fixedassets = models.FloatField(db_column='fixedAssets', blank=True, null=True)  # Field name made lowercase.
    reserved = models.FloatField(blank=True, null=True)
    reservedpershare = models.FloatField(db_column='reservedPerShare', blank=True, null=True)  # Field name made lowercase.
    esp = models.FloatField(blank=True, null=True)
    bvps = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    timetomarket = models.BigIntegerField(db_column='timeToMarket', blank=True, null=True)  # Field name made lowercase.
    undp = models.FloatField(blank=True, null=True)
    perundp = models.FloatField(blank=True, null=True)
    rev = models.FloatField(blank=True, null=True)
    profit = models.FloatField(blank=True, null=True)
    gpr = models.FloatField(blank=True, null=True)
    npr = models.FloatField(blank=True, null=True)
    holders = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'finweb_stockdata'


class Profitdata(models.Model):
    index = models.BigIntegerField(blank=True,primary_key=True)
    unnamed_0 = models.BigIntegerField(db_column='Unnamed: 0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    code = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True)
    roe = models.FloatField(blank=True, null=True)
    net_profit_ratio = models.FloatField(blank=True, null=True)
    gross_profit_rate = models.FloatField(blank=True, null=True)
    net_profits = models.FloatField(blank=True, null=True)
    eps = models.FloatField(blank=True, null=True)
    business_income = models.FloatField(blank=True, null=True)
    bips = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'finweb_profitdata'


class Reportdata(models.Model):
    index = models.BigIntegerField(blank=True,primary_key=True)
    unnamed_0 = models.BigIntegerField(db_column='Unnamed: 0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    code = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True)
    eps = models.FloatField(blank=True, null=True)
    eps_yoy = models.FloatField(blank=True, null=True)
    bvps = models.FloatField(blank=True, null=True)
    roe = models.FloatField(blank=True, null=True)
    epcf = models.FloatField(blank=True, null=True)
    net_profits = models.FloatField(blank=True, null=True)
    profits_yoy = models.FloatField(blank=True, null=True)
    distrib = models.TextField(blank=True)
    report_date = models.TextField(blank=True)

    class Meta:
        managed = True
        db_table = 'finweb_reportdata'

class Growthdata(models.Model):
    index = models.BigIntegerField(blank=True,primary_key=True)
    unnamed_0 = models.BigIntegerField(db_column='Unnamed: 0', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    code = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True)
    mbrg = models.FloatField(blank=True, null=True)
    nprg = models.FloatField(blank=True, null=True)
    nav = models.FloatField(blank=True, null=True)
    targ = models.FloatField(blank=True, null=True)
    epsg = models.FloatField(blank=True, null=True)
    seg = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'finweb_growthdata'

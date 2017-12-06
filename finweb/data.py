# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
#from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FinwebGrowthdata(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
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
        managed = False
        db_table = 'finweb_growthdata'


class FinwebPortfolio(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    list = models.TextField()
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'finweb_portfolio'


class FinwebProfitdata(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
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
        managed = False
        db_table = 'finweb_profitdata'


class FinwebReportdata(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
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
        managed = False
        db_table = 'finweb_reportdata'


class FinwebStockdata(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
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
        managed = False
        db_table = 'finweb_stockdata'


class FinwebUserprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    gender = models.CharField(max_length=5)
    phonenum = models.CharField(max_length=15)
    birthday = models.DateField()
    list = models.TextField()
    user = models.ForeignKey(AuthUser, unique=True)

    class Meta:
        managed = False
        db_table = 'finweb_userprofile'

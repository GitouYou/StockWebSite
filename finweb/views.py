# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from finweb.forms import UserForm,UserProfileForm,LoginForm,changepasswordForm
import urllib2,re
import tushare as ts
from finweb.models import UserProfile,Portfolio,Stockdata,Profitdata,Reportdata,Growthdata
from django.contrib.auth.models import User
import random,datetime,os
from django.conf import settings
import rpy2.robjects as ro
import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt
import scipy.optimize as sco


# Create your views here.
def index(request):
    a = ts.get_latest_news(top= 6 ,show_content=True)
    news_list1 = []
    news_list2 = []
    for i in range(3):
        dic1 = {}
        dic1['classify'] = a.ix[i]['classify']
        dic1['title']=a.ix[i]['title']
        dic1['time']=a.ix[i]['time']
        dic1['url']=a.ix[i]['url']
        dic1['content']=a.ix[i]['content'][0:100]+"....."
        dic2 = {}
        dic2['classify'] = a.ix[i+3]['classify']
        dic2['title']=a.ix[i+3]['title']
        dic2['time']=a.ix[i+3]['time']
        dic2['url']=a.ix[i+3]['url']
        dic2['content']=a.ix[i+3]['content'][0:100]+"....."
        news_list1.append(dic1)
        news_list2.append(dic2)
    return render(request,'finweb/index.html',{'news_list1':news_list1,'news_list2':news_list2})


def register(request):
    username=''
    password=''
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        rulesagree = request.POST.get('rulesagree',u'')
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        passwd_errors = u''
        rules_errors = u''
        flag = False
        if not password == password_again:
            print "password\n"
            passwd_errors = u'两次密码输入不一致'
            flag = True
        if not rulesagree == u"True":
            print "rulesagree\n"
            rules_errors = u'请阅读并同意相关条款'
            flag = True
        if flag:
            return render(request,'finweb/register.html',{'userform':user_form,'profileform':profile_form,'passwd_errors':passwd_errors,'rules_errors':rules_errors})

        if user_form.is_valid() and profile_form.is_valid():
            #当user已经注册的时候
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return HttpResponseRedirect('/finweb/')
            else:
                print "User fail\n"
        else:
            print user_form.errors,profile_form.errors
            return render(request,'finweb/register.html',{'userform':user_form,'profileform':profile_form,'passwd_errors':passwd_errors,'rules_errors':rules_errors})

    else:
        return render(request,'finweb/register.html',{})


def user_login(request):
    if request.method =='POST':
        loginform = LoginForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if loginform.is_valid():
            user = authenticate(username=username,password=password)

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/finweb/')
            else:
                return HttpResponse("No Longer Active Account!")

        else:
            print loginform.errors
            return render(request,'finweb/login.html', {'form': loginform })
    else:
        return render(request,'finweb/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/finweb/')


def get_index_data(request):
    ind = request.GET.get('index','000001')
    index_data = ts.get_k_data(ind,index=True)
    index_no_code = index_data.loc[:,['date','open','close','high','low']]
    data = index_no_code.to_json(orient="values")
    return JsonResponse(data,safe=False)

def getUrlByCode(code):
    """根据代码获取详细的url"""
    url = ''
    stockCode = ''
    if code == '000001':
        url = 'http://hq.sinajs.cn/list=s_sh000001'
    elif code == '399001':
        url = 'http://hq.sinajs.cn/list=s_sz399001'
    elif code == '399006':
        url = 'http://hq.sinajs.cn/list=s_sz399006'
    else:
        pattern = re.compile(r'^60*')
        match = pattern.match(code)
        if match:
            stockCode = 'sh'+ code
        else:
            stockCode = 'sz' + code
        url = 'http://hq.sinajs.cn/list=s_'+stockCode

    return url
def get_span_data(request):
    ind = request.GET.get('index','000001')
    url = getUrlByCode(ind)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    stockStr = response.read()
    stockList = stockStr.split('"')
    stockList = stockList[1].split(',')
    stockDic = {}
    stockDic['now'] = round(float(stockList[1]),2)
    stockDic['change']=round(float(stockList[2]),2)
    stockDic['percent'] = float(stockList[3])
    stockDic['volumn']= round(float(stockList[4])/pow(10,6),2)
    stockDic['amount']= round(float(stockList[5])/pow(10,4),2)
    return JsonResponse(stockDic,safe=False)

def rules(request):
    return render(request,'finweb/rules.html',{})

@login_required
def userinfo(request):
    user_exist = User.objects.get(username=request.user.username)
    user = User.objects.filter(username=request.user.username)
    profile = UserProfile.objects.filter(user = user)
    info_dic = {}
    if user_exist and profile:
        info_dic['username'] = request.user.username
        info_dic['email'] = user[0].email
        info_dic['gender'] = profile[0].gender
        info_dic['phonenum'] = profile[0].phonenum
        info_dic['birthday'] = profile[0].birthday
    return render(request,'finweb/userinfo.html',{'info_dic':info_dic})

@login_required
def changepassword(request):
    result = False
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        password = request.POST.get('password')
        check = authenticate(username=request.user.username,password=oldpassword)
        if not check:
                passwd_errors = u'原密码错误'
                return render(request,'finweb/changepassword.html',{'passwd_errors':passwd_errors})
        form = changepasswordForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(password)
            user.save()
            result = True
            return render(request,'finweb/changepassword.html',{'result':result})
        else:
            return render(request,'finweb/changepassword.html',{'form':form})
    else:
        return render(request,'finweb/changepassword.html',{})

@login_required
def changeinfo(request):
    result = False
    if request.method=='POST':
        new_info_dic = {}
        new_username = request.POST.get('username')
        new_gender = request.POST.get('gender')
        new_phonenum = request.POST.get('phonenum')
        new_brithday = request.POST.get('birthday')
        new_info_dic['username'] = new_username
        new_info_dic['gender'] = new_gender
        new_info_dic['phonenum'] = new_phonenum
        new_info_dic['birthday'] = new_brithday
        print new_info_dic
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            # print "both valid!!"
            user = User.objects.get(username=request.user.username)
            profile = UserProfile.objects.get(user = user)
            #修改信息并保存
            # print "before change!"
            if new_username == u'':
                username_error = u'用户名不能为空'
                return render(request,'finweb/changeinfo.html',{'info_dic':new_info_dic,'profileform':profile_form,'username_err':username_error})
            if request.user.username != new_username:
                username_exist = User.objects.filter(username= new_username).exists()
                if username_exist:
                    username_error = u"用户名已存在，请更改"
                    return render(request,'finweb/changeinfo.html',{'info_dic':new_info_dic,'profileform':profile_form,'username_error':username_error})
                user.username = new_username
                user.save()
                profile.user = user
                # print "change user"
            profile.gender = new_gender
            profile.phonenum = new_phonenum
            profile.birthday = new_brithday
            profile.save()
            # print "change profile"
            result = True
            return render(request,'finweb/changeinfo.html',{'info_dic':new_info_dic,'profileform':profile_form,'result':result})

        else:
            # print "errors!!"
            print profile_form.errors
            print "IN ELSE!!\n"
            return render(request,'finweb/changeinfo.html',{'info_dic':new_info_dic,'profileform':profile_form,'result':result})
    else:
        # print "Get!!"
        user = User.objects.filter(username=request.user.username)
        profile = UserProfile.objects.filter(user = user)
        info_dic = {}
        if user and profile:
            info_dic['username'] = request.user.username
            info_dic['gender'] = profile[0].gender
            info_dic['phonenum'] = profile[0].phonenum
            #注意此处需要更改格式
            info_dic['birthday'] = profile[0].birthday.strftime("%Y-%m-%d")
            return render(request,'finweb/changeinfo.html',{'info_dic':info_dic})


def operate(request):
    result = True
    if request.method=='POST':
        code = request.POST.get("code")
        try:
            stock = Stockdata.objects.filter(code=code).exists()
        except:
            result = False
            return render(request,'finweb/operate.html',{'result':result})
        if not stock:
            # print "in false haha"
            result = False
            return render(request,'finweb/operate.html',{'result':result})
        request.session['code'] = code
        request.session['is_from_stocks'] = False
        # print "session set!!",request.session.get('code',default=None)
        #注意redirect网址的书写形式，最前面有/，最后没有.html
        return HttpResponseRedirect('/finweb/stockinfo')
    else:
         return render(request,'finweb/operate.html',{})

    return render(request,'finweb/operate.html',{})




def stocks(request):
    stock_list = []
    portfolio_list = []
    # print "before get user*******\n"
    user = User.objects.get(username=request.user.username)
    # print "before print userid*********\n"
    # print str(user.id)
    profile = UserProfile.objects.get(user_id=user.id)
    list_str = str(profile.list)
    list = list_str.split(';')
    print list
    if list and list[0]=='':
        # print "inside if!!!"
        stock_list = []
    else:
        data =ts.get_realtime_quotes(list)
        # print data.ix[0]['price']
        new_data = data.loc[:,['name','price','open','pre_close','high','low']]
        for i in range(len(list)):
            # print "inside range!!"
            dic = {}
            dic['code'] = list[i]
            dic['name'] = new_data.ix[i]['name']
            dic['price'] = round(float(new_data.ix[i]['price']),2)
            dic['open'] = round(float(new_data.ix[i]['open']),2)
            dic['pre_close'] = round(float(new_data.ix[i]['pre_close']),2)
            dic['high'] = round(float(new_data.ix[i]['high']),2)
            dic['low'] = round(float(new_data.ix[i]['low']),2)
            dic['updown'] = round(float(new_data.ix[i]['price']) - float(new_data.ix[i]['pre_close']),2)
            dic['percent'] = str(round(dic['updown']/dic['pre_close']*100,2))+"%"
            stock_list.append(dic)
    port = Portfolio.objects.filter(user_id=user.id)
    for p in port:
        dic = {}
        dic['name'] = p.name
        portfolio_list.append(dic)

    return render(request,'finweb/stocks.html',{'stock_list':stock_list,'portfolio_list':portfolio_list})

def get_stocks_data(request):
    stock_list = []
    user = User.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user_id=user.id)
    list_str = str(profile.list)
    list = list_str.split(';')
    if list and list[0]=='':
        stock_list = []
    else:
        data =ts.get_realtime_quotes(list)
        new_data = data.loc[:,['code','price','high','low','pre_close']]
        for i in range(len(list)):
            dic = {}
            dic['code'] = list[i]
            dic['price'] = round(float(new_data.ix[i]['price']),2)
            dic['high'] = round(float(new_data.ix[i]['high']),2)
            dic['low'] = round(float(new_data.ix[i]['low']),2)
            dic['pre_close'] = round(float(new_data.ix[i]['pre_close']),2)
            dic['updown'] = round(float(new_data.ix[i]['price']) - float(new_data.ix[i]['pre_close']),2)
            dic['percent'] = str(round(dic['updown']/dic['pre_close']*100,2))+"%"
            if dic['high'] >= dic['pre_close']:
                dic['high_red'] = True
            else:
                dic['high_red'] = False
            if dic['low'] >= dic['pre_close']:
                dic['low_red'] = True
            else:
                dic['low_red'] = False
            stock_list.append(dic)
    return JsonResponse(stock_list,safe=False)

def stocks_to_info(request):
    dic = {}
    dic['result'] = False
    code = request.GET.get('code','')
    request.session['code'] = code
    request.session['is_from_stocks'] = True
    dic['result'] = True
    return JsonResponse(dic,safe=False)

def delete_stocks(request):
    dic = {}
    list_str = request.GET.get('list_str','')
    delete_list = list_str.split(';')
    dic['empty'] = False
    dic['result'] = False
    if delete_list and delete_list[0]=='':
        dic['empty'] = True
        return JsonResponse(dic,safe=False)
    user = User.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user_id=user.id)
    list_str2 = str(profile.list)
    all_list = list_str2.split(';')
    # print all_list
    # print "\n***********\n"
    # print delete_list
    for i in range(len(delete_list)):
        all_list.remove(delete_list[i])
    # print "\nafter delete\n"
    # print all_list
    new_str = ";".join(all_list)
    # print "new_str:"+new_str
    profile.list = new_str
    profile.save()
    dic['result'] = True
    return JsonResponse(dic,safe=False)

def add_stocks_toport(request):
    dic = {}
    list_str = request.GET.get('list_str','')
    p_name = request.GET.get('portfolio','')
    add_list = list_str.split(';')
    dic['empty'] = False
    dic['result'] = False
    if add_list and add_list[0]=='':
        dic['empty'] = True
        return JsonResponse(dic,safe=False)
    user = User.objects.get(username=request.user.username)
    portfolio = Portfolio.objects.get(user_id=user.id,name=p_name)
    list_str2 = str(portfolio.list)
    all_list = list_str2.split(';')
    if len(all_list)==1 and all_list[0]=='':
        all_list = []
    for i in range(len(add_list)):
        all_list.append(add_list[i])
    print all_list
    new_list ={}.fromkeys(all_list).keys()
    new_str = ";".join(new_list)
    # print "new_str:"+new_str
    portfolio.list = new_str
    portfolio.save()
    dic['result'] = True
    return JsonResponse(dic,safe=False)

def portfolio(request):
    #股票代码前面的0被去掉的问题
    #部分数据位null，被读取出来怎么办
    big_list = []
    user = User.objects.get(username=request.user.username)
    port = Portfolio.objects.filter(user_id=user.id).exists()
    #用户还没创建投资组合，big_list为空
    if not port:
         return render(request,'finweb/portfolio.html',{'big_list':big_list })
    p_query =  Portfolio.objects.filter(user_id=user.id)
    for p in p_query:
        data_list = []
        big_dic = {} # name,data
        p_str = str(p.list)
        p_name = p.name
        p_list = p_str.split(';')
        if p_list and p_list[0]== '':
            #只有组合名，还未添加股票
            big_dic['name'] = p_name
            big_dic['data'] = data_list
        else:
            big_dic['name'] = p_name
            for pp in p_list:
                data_dic = {} #code nam pe pb ...
                data_dic['code'] = pp
                if Stockdata.objects.filter(code=pp).exists():
                    s_result = Stockdata.objects.filter(code =pp)
                    #如果此处查询出的值为空怎么办！！！！！！！！
                    data_dic['name']= s_result[0].name
                    data_dic['pe'] = s_result[0].pe
                    data_dic['pb']= s_result[0].pb
                    data_dic['esp']= s_result[0].esp
                    data_dic['bvps']= s_result[0].bvps
                else:
                    data_dic['pe'] = '--'
                    data_dic['pb']= '--'
                    data_dic['esp']= '--'
                    data_dic['bvps']= '--'
                if Reportdata.objects.filter(code=pp).exists():
                    r_result = Reportdata.objects.filter(code=pp)
                    data_dic['roe'] = r_result[0].roe
                    data_dic['net_profits'] = r_result[0].net_profits
                    data_dic['profits_yoy'] = r_result[0].profits_yoy
                else:
                    data_dic['roe'] = '--'
                    data_dic['net_profits'] = '--'
                    data_dic['profits_yoy'] = '--'
                if Profitdata.objects.filter(code=pp).exists():
                    p_result = Profitdata.objects.filter(code=pp)
                    data_dic['income'] = p_result[0].business_income
                else:
                    data_dic['income'] = '--'

                for k in data_dic.keys():
                    if not data_dic[k]:
                        data_dic[k] = '--'
                data_list.append(data_dic)
            big_dic['data'] = data_list
        big_list.append(big_dic)
    return render(request,'finweb/portfolio.html',{'big_list':big_list })

def port_to_info(request):
    dic = {}
    dic['result'] = False
    code = request.GET.get('code','')
    request.session['code'] = code
    request.session['is_from_stocks'] = False
    dic['result'] = True
    return JsonResponse(dic,safe=False)

def delete_stocks_inp(request):
    dic = {}
    list_str = request.GET.get('list_str','')
    name = request.GET.get('name','')
    delete_list = list_str.split(';')
    dic['empty'] = False
    dic['result'] = False
    if delete_list and delete_list[0]=='':
        dic['empty'] = True
        return JsonResponse(dic,safe=False)
    user = User.objects.get(username=request.user.username)
    port = Portfolio.objects.get(user_id=user.id,name=name)
    list_str2 = str(port.list)
    all_list = list_str2.split(';')
    # print all_list
    # print "\n***********\n"
    print delete_list
    for i in range(len(delete_list)):
        all_list.remove(delete_list[i])
    # print "\nafter delete\n"
    # print all_list
    new_str = ";".join(all_list)
    # print "new_str:"+new_str
    port.list = new_str
    port.save()
    dic['result'] = True
    return JsonResponse(dic,safe=False)

def delete_portfolio(request):
    dic = {}
    name = request.GET.get('name','')
    dic['result'] = False
    user = User.objects.get(username=request.user.username)
    Portfolio.objects.filter(user_id=user.id,name=name).delete()
    dic['result'] = True
    return JsonResponse(dic,safe=False)


def add_portfolio(request):
    #name 不允许重复
    result = True
    if request.method=='POST':
        p_name = request.POST.get("p_name")
        user = User.objects.get(username=request.user.username)
        port = Portfolio.objects.filter(user_id=user.id,name=p_name).exists()
        if port:
            result = False
            return render(request,'finweb/add_portfolio.html',{'result':result})
        obj = Portfolio(user_id=user.id,name=p_name,list='')
        obj.save()
        return render(request,'finweb/add_portfolio.html',{'result':result})
    else:
         return render(request,'finweb/add_portfolio.html',{})



def stockinfo(request):
    #stock
    #name code price percent updown open pre_close high low day_url
    #is_from_stocks
    #搜素返回result
    #portfolio_list
    is_from_stocks = request.session.get('is_from_stocks',False)
    sample = random.sample(xrange(Stockdata.objects.count()),1)
    random_sample = Stockdata.objects.all()[sample[0]]
    random_code = random_sample.code
    code = request.session.get('code',random_code)
    stock = {}
    portfolio_list = []
    user = User.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user_id=user.id)
    list_str = str(profile.list)
    list = list_str.split(';')
    print code
    print "\n"+"******"+ str(code)+"\n"
    if list and list[0]=='':
        is_from_stocks = False
    elif code in list:
        is_from_stocks = True
    port = Portfolio.objects.filter(user_id=user.id)
    for p in port:
        dic = {}
        dic['name'] = p.name
        portfolio_list.append(dic)
    data =ts.get_realtime_quotes(code)
    stock['code'] = code
    stock['name'] = data.ix[0]['name']
    stock['price'] = round(float(data.ix[0]['price']),2)
    stock['open'] = round(float(data.ix[0]['open']),2)
    stock['pre_close'] = round(float(data.ix[0]['pre_close']),2)
    stock['high'] = round(float(data.ix[0]['high']),2)
    stock['low'] = round(float(data.ix[0]['low']),2)
    stock['updown'] = round(float(data.ix[0]['price']) - float(data.ix[0]['pre_close']),2)
    stock['percent'] = str(round(stock['updown']/stock['pre_close']*100,2))+"%"
    stockCode =''
    pattern = re.compile(r'^60*')
    match = pattern.match(code)
    if match:
        stockCode = 'sh'+ code
    else:
        stockCode = 'sz' + code
    url = 'http://image.sinajs.cn/newchart/min/n/'+stockCode+'.gif'
    stock['day_url'] = url

    return render(request,'finweb/stockinfo.html',{'stock':stock,'is_from_stocks':is_from_stocks,'portfolio_list':portfolio_list})

def get_info_stockdata(request):
    code = request.session.get('code','')
    data =ts.get_realtime_quotes(code)
    new_data = data.loc[:,['code','price','high','low','pre_close']]
    dic = {}
    dic['price'] = round(float(new_data.ix[0]['price']),2)
    dic['high'] = round(float(new_data.ix[0]['high']),2)
    dic['low'] = round(float(new_data.ix[0]['low']),2)
    dic['pre_close'] = round(float(new_data.ix[0]['pre_close']),2)
    dic['updown'] = round(float(new_data.ix[0]['price']) - float(new_data.ix[0]['pre_close']),2)
    dic['percent'] = str(round(dic['updown']/dic['pre_close']*100,2))+"%"
    if dic['high'] >= dic['pre_close']:
        dic['high_red'] = True
    else:
        dic['high_red'] = False
    if dic['low'] >= dic['pre_close']:
        dic['low_red'] = True
    else:
        dic['low_red'] = False
    return JsonResponse(dic,safe=False)

def get_info_kdata(request):
    code = request.session.get('code','')
    # print code
    # print type(code)
    # print "********\n"
    code_data = ts.get_k_data(str(code))
    # print "******** get_k_data\n"
    index_no_code = code_data.loc[:,['date','open','close','high','low']]
    # print "******** index no code\n"
    data = index_no_code.to_json(orient="values")
    # print "******** to json\n"
    return JsonResponse(data,safe=False)

def get_info_search(request):
    result = True
    dic = {}
    code = request.GET.get('code','')
    try:
        stock = Stockdata.objects.filter(code=code).exists()
    except:
        result = False
        dic['result'] = result
        return JsonResponse(dic,safe=False)

    if not stock:
        result = False
    else:
        request.session['code'] = code
        request.session['is_from_stocks'] = False
    # print result
    # print "\n"
    dic['result'] = result
    return JsonResponse(dic,safe=False)

def addto_stocks(request):
    dic = {}
    list_str = request.GET.get('code','')
    add_list = list_str.split(';')
    dic['result'] = False
    if add_list and add_list[0]=='':
        return JsonResponse(dic,safe=False)
    user = User.objects.get(username=request.user.username)
    p = UserProfile.objects.get(user_id=user.id)
    list_str2 = str(p.list)
    all_list = list_str2.split(';')
    if all_list and all_list[0]=='':
        all_list=[]
    for i in range(len(add_list)):
        all_list.append(add_list[i])
    new_list ={}.fromkeys(all_list).keys()
    new_str = ";".join(new_list)
    # print "************",new_str
    p.list = new_str
    p.save()
    dic['result'] = True
    return JsonResponse(dic,safe=False)

def indicator(request):
  code = request.session.get('code')
  query = Stockdata.objects.filter(code=code)
  name = query[0].name
  stock = {}
  stock['code'] = code
  stock['name'] = name
  return render(request,'finweb/indicator.html',{'stock':stock})

def single_get_first(unicode1):
  str1 = unicode1.encode('gbk')
  try:
    ord(str1)
    return str1
  except:
    asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
    if asc >= -20319 and asc <= -20284:
      return 'a'
    if asc >= -20283 and asc <= -19776:
      return 'b'
    if asc >= -19775 and asc <= -19219:
      return 'c'
    if asc >= -19218 and asc <= -18711:
      return 'd'
    if asc >= -18710 and asc <= -18527:
      return 'e'
    if asc >= -18526 and asc <= -18240:
      return 'f'
    if asc >= -18239 and asc <= -17923:
      return 'g'
    if asc >= -17922 and asc <= -17418:
      return 'h'
    if asc >= -17417 and asc <= -16475:
      return 'j'
    if asc >= -16474 and asc <= -16213:
      return 'k'
    if asc >= -16212 and asc <= -15641:
      return 'l'
    if asc >= -15640 and asc <= -15166:
      return 'm'
    if asc >= -15165 and asc <= -14923:
      return 'n'
    if asc >= -14922 and asc <= -14915:
      return 'o'
    if asc >= -14914 and asc <= -14631:
      return 'p'
    if asc >= -14630 and asc <= -14150:
      return 'q'
    if asc >= -14149 and asc <= -14091:
      return 'r'
    if asc >= -14090 and asc <= -13119:
      return 's'
    if asc >= -13118 and asc <= -12839:
      return 't'
    if asc >= -12838 and asc <= -12557:
      return 'w'
    if asc >= -12556 and asc <= -11848:
      return 'x'
    if asc >= -11847 and asc <= -11056:
      return 'y'
    if asc >= -11055 and asc <= -10247:
      return 'z'
    return ''

def multi_get_letter(str_input):
  if isinstance(str_input, unicode):
    unicode_str = str_input
  else:
    try:
      unicode_str = str_input.decode('utf8')
    except:
      try:
        unicode_str = str_input.decode('gbk')
      except:
        print 'unknown coding'
        return
  return_list = []
  for one_unicode in unicode_str:
    return_list.append(single_get_first(one_unicode))
  return return_list

def get_character(str_input):
  a = multi_get_letter(str_input)
  b = ''
  for i in a:
    b= b+i
  return b.upper()


def get_macd(request):
    time = request.GET.get('time','3')
    code = request.session.get('code')
    to = datetime.datetime.now().strftime("%Y-%m-%d")
    BASE_DIR = settings.BASE_DIR  # 项目目录
    # 图片放在static/pics/里面
    PICS = os.path.join(BASE_DIR, 'static','finweb','pics')
    filestr = '{code}_macd_{time}_{to}'.format(code=code,time=time,to=to)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    if result_list:
        return JsonResponse(result_list,safe=False)
    d = 30
    if time == '3':
        d = 91
    elif time =='6':
        d = 182
    elif time=='12':
        d = 365
    fromdate = datetime.date.today() - datetime.timedelta(days=d)
    fr = fromdate.strftime("%Y-%m-%d")
    # BASE_DIR = settings.BASE_DIR  # 项目目录
    # PICS = os.listdir(os.path.join(BASE_DIR, 'static','finweb','pics'))
    PICS_R = PICS.replace("\\","/")
    pattern = re.compile(r'^60*')
    match = pattern.match(code)
    if match:
        stockCode = code + '.ss'
    else:
        stockCode = code + '.sz'

    stock = Stockdata.objects.filter(code=code)
    name = stock[0].name
    mark = get_character(name)
    ####
    filename = "{mark}.csv".format(mark=mark)
    csv_path = PICS+'/'+filename
    data= ts.get_k_data(code,start=fr,end=to)
    data = data.loc[:,['date','open','high','low','close','volume']]
    data['adjusted']=data['close']
    data.reset_index(drop=True)
    data.to_csv(csv_path,index=False)
    # R语言中设置目录为反斜杠
    try:
        ro.r(
           '''
           setwd('{PICS}')
           rm(list=ls())
           suppressPackageStartupMessages(library('quantmod',warn.conflicts = FALSE))
           options(warn = -1)
           options("getSymbols.warning4.0"=FALSE)
           setSymbolLookup({mark}=list(name='{stockCode}',src='csv',from="{fr}",to="{to}"))
           getSymbols("{mark}")
           jpeg(file="{code}_macd_{time}_{to}.jpeg",width = 650,height = 360)
           chartSeries({mark},up.col='red',dn.col='green',TA="addVo();addMACD();")
           dev.off()
           q()
           '''.format(PICS=PICS_R,mark=mark,code=code,time=time,stockCode=stockCode,fr=fr,to= to )
             )
    except:
        print "Error in R !\n"
        result_list = ['bug.jpeg']
        return JsonResponse(result_list,safe=False)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    return JsonResponse(result_list,safe=False)

def get_adx(request):
    time = request.GET.get('time','3')
    code = request.session.get('code')
    to = datetime.datetime.now().strftime("%Y-%m-%d")
    BASE_DIR = settings.BASE_DIR  # 项目目录
    # 图片放在static/pics/里面
    PICS = os.path.join(BASE_DIR, 'static','finweb','pics')
    filestr = '{code}_adx_{time}_{to}'.format(code=code,time=time,to=to)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    if result_list:
        return JsonResponse(result_list,safe=False)
    d = 30
    if time == '3':
        d = 91
    elif time =='6':
        d = 182
    elif time=='12':
        d = 365
    fromdate = datetime.date.today() - datetime.timedelta(days=d)
    fr = fromdate.strftime("%Y-%m-%d")
    PICS_R = PICS.replace("\\","/")
    pattern = re.compile(r'^60*')
    match = pattern.match(code)
    if match:
        stockCode = code + '.ss'
    else:
        stockCode = code + '.sz'

    stock = Stockdata.objects.filter(code=code)
    name = stock[0].name
    mark = get_character(name)
    filename = "{mark}.csv".format(mark=mark)
    csv_path = PICS+'/'+filename
    data= ts.get_k_data(code,start=fr,end=to)
    data = data.loc[:,['date','open','high','low','close','volume']]
    data['adjusted']=data['close']
    data.reset_index(drop=True)
    data.to_csv(csv_path,index=False)
    # R语言中设置目录为反斜杠
    try:
        ro.r(
           '''
           setwd('{PICS}')
           rm(list=ls())
           suppressPackageStartupMessages(library('quantmod',warn.conflicts = FALSE))
           options(warn =-1)
           options("getSymbols.warning4.0"=FALSE)
           setSymbolLookup({mark}=list(name='{stockCode}',src='csv',from="{fr}",to="{to}"))
           getSymbols("{mark}")
           jpeg(file="{code}_adx_{time}_{to}.jpeg",width = 650,height = 360)
           chartSeries({mark},up.col='red',dn.col='green',TA="addVo();addADX();")
           dev.off()
           q()
           '''.format(PICS=PICS_R,mark=mark,code=code,time=time,stockCode=stockCode,fr=fr,to= to )
             )
    except:
        print "Error in R !\n"
        result_list = ['bug.jpeg']
        return JsonResponse(result_list,safe=False)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    return JsonResponse(result_list,safe=False)

def get_sma(request):
    time = request.GET.get('time','3')
    code = request.session.get('code')
    to = datetime.datetime.now().strftime("%Y-%m-%d")
    BASE_DIR = settings.BASE_DIR  # 项目目录
    # 图片放在static/pics/里面
    PICS = os.path.join(BASE_DIR, 'static','finweb','pics')
    filestr = '{code}_sma_{time}_{to}'.format(code=code,time=time,to=to)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    if result_list:
        return JsonResponse(result_list,safe=False)
    d = 30
    if time == '3':
        d = 91
    elif time =='6':
        d = 182
    elif time=='12':
        d = 365
    fromdate = datetime.date.today() - datetime.timedelta(days=d)
    fr = fromdate.strftime("%Y-%m-%d")
    PICS_R = PICS.replace("\\","/")
    pattern = re.compile(r'^60*')
    match = pattern.match(code)
    if match:
        stockCode = code + '.ss'
    else:
        stockCode = code + '.sz'

    stock = Stockdata.objects.filter(code=code)
    name = stock[0].name
    mark = get_character(name)
    filename = "{mark}.csv".format(mark=mark)
    csv_path = PICS+'/'+filename
    data= ts.get_k_data(code,start=fr,end=to)
    data = data.loc[:,['date','open','high','low','close','volume']]
    data['adjusted']=data['close']
    data.reset_index(drop=True)
    data.to_csv(csv_path,index=False)
    # R语言中设置目录为反斜杠
    try:
        ro.r(
           '''
           setwd('{PICS}')
           rm(list=ls())
           suppressPackageStartupMessages(library('quantmod',warn.conflicts = FALSE))
           options(warn =-1)
           options("getSymbols.warning4.0"=FALSE)
           setSymbolLookup({mark}=list(name='{stockCode}',src='csv',from="{fr}",to="{to}"))
           getSymbols("{mark}",warnings= FALSE)
           jpeg(file="{code}_sma_{time}_{to}.jpeg",width = 650,height = 360)
           chartSeries({mark},up.col='red',dn.col='green',TA="addVo();addSMA(n=10);")
           dev.off()
           '''.format(PICS=PICS_R,mark=mark,code=code,time=time,stockCode=stockCode,fr=fr,to= to )
             )
    except:
        print "Error in R !\n"
        result_list = ['bug.jpeg']
        return JsonResponse(result_list,safe=False)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    return JsonResponse(result_list,safe=False)

def get_bbands(request):
    time = request.GET.get('time','3')
    code = request.session.get('code')
    to = datetime.datetime.now().strftime("%Y-%m-%d")
    BASE_DIR = settings.BASE_DIR  # 项目目录
    # 图片放在static/pics/里面
    PICS = os.path.join(BASE_DIR, 'static','finweb','pics')
    filestr = '{code}_bbands_{time}_{to}'.format(code=code,time=time,to=to)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    if result_list:
        return JsonResponse(result_list,safe=False)
    d = 30
    if time == '3':
        d = 91
    elif time =='6':
        d = 182
    elif time=='12':
        d = 365
    fromdate = datetime.date.today() - datetime.timedelta(days=d)
    fr = fromdate.strftime("%Y-%m-%d")
    PICS_R = PICS.replace("\\","/")
    pattern = re.compile(r'^60*')
    match = pattern.match(code)
    if match:
        stockCode = code + '.ss'
    else:
        stockCode = code + '.sz'

    stock = Stockdata.objects.filter(code=code)
    name = stock[0].name
    mark = get_character(name)
    filename = "{mark}.csv".format(mark=mark)
    csv_path = PICS+'/'+filename
    data= ts.get_k_data(code,start=fr,end=to)
    data = data.loc[:,['date','open','high','low','close','volume']]
    data['adjusted']=data['close']
    data.reset_index(drop=True)
    data.to_csv(csv_path,index=False)
    # R语言中设置目录为反斜杠
    try:
        ro.r(
           '''
           setwd('{PICS}')
           rm(list=ls())
           suppressPackageStartupMessages(library('quantmod',warn.conflicts = FALSE))
           options(warn =-1)
           options("getSymbols.warning4.0"=FALSE)
           setSymbolLookup({mark}=list(name='{stockCode}',src='csv',from="{fr}",to="{to}"))
           getSymbols("{mark}")
           jpeg(file="{code}_bbands_{time}_{to}.jpeg",width = 650,height = 360)
           chartSeries({mark},up.col='red',dn.col='green',TA="addVo();addBBands(n=10,sd=2,draw=\'bands\')")
           dev.off()
           '''.format(PICS=PICS_R,mark=mark,code=code,time=time,stockCode=stockCode,fr=fr,to= to )
             )
    except:
        print "Error in R !\n"
        result_list = ['bug.jpeg']
        return JsonResponse(result_list,safe=False)
    list = os.listdir(PICS)
    result_list = filter(lambda x: x.startswith(filestr),list)
    return JsonResponse(result_list,safe=False)



def fin_data(request):
  code = request.session.get('code')
  query = Stockdata.objects.filter(code=code)
  name = query[0].name
  stock = {}
  stock['code'] = code
  stock['name'] = name
  basic_dic = {}
  report_dic = {}
  profit_dic = {}
  growth_dic = {}
  if Stockdata.objects.filter(code = code).exists():
      s_result = Stockdata.objects.filter(code =code)
      #如果此处查询出的值为空怎么办！！！！！！！！
      basic_dic['industry']= s_result[0].industry
      basic_dic['area'] = s_result[0].area
      basic_dic['pe'] = s_result[0].pe
      basic_dic['pb']= s_result[0].pb
      basic_dic['gpr']= s_result[0].gpr
      basic_dic['npr']= s_result[0].npr
      basic_dic['esp']= s_result[0].esp
      basic_dic['perundp']= s_result[0].perundp
      basic_dic['bvps']= s_result[0].bvps
      basic_dic['reservedpershare']= s_result[0].reservedpershare
      basic_dic['rev']= s_result[0].rev
      basic_dic['profit']= s_result[0].profit

  else:
      basic_dic['industry']= "--"
      basic_dic['area'] ="--"
      basic_dic['pe'] = "--"
      basic_dic['pb']="--"
      basic_dic['gpr']= "--"
      basic_dic['npr']= "--"
      basic_dic['esp']= "--"
      basic_dic['perundp']= '--'
      basic_dic['bvps']= "--"
      basic_dic['reservedpershare']= "--"
      basic_dic['rev']= "--"
      basic_dic['profit']= '--'

  for k in basic_dic.keys():
      if not basic_dic[k]:
          basic_dic[k] = '--'

  if Reportdata.objects.filter(code=code).exists():
      r_result = Reportdata.objects.filter(code=code)
      report_dic['roe'] = r_result[0].roe
      report_dic['net_profits'] = r_result[0].net_profits
      report_dic['profits_yoy'] = r_result[0].profits_yoy
      report_dic['epcf'] = r_result[0].epcf
      report_dic['bvps'] = r_result[0].bvps
  else:
      report_dic['roe'] = '--'
      report_dic['net_profits'] = '--'
      report_dic['profits_yoy'] = '--'
      report_dic['epcf'] = '--'
      report_dic['bvps'] = '--'

  for k in report_dic.keys():
      if not report_dic[k]:
          report_dic[k] = '--'

  if Profitdata.objects.filter(code=code).exists():
      p_result = Profitdata.objects.filter(code=code)
      profit_dic['business_income'] = p_result[0].business_income
      profit_dic['bips'] = p_result[0].bips
  else:
      profit_dic['business_income'] ='--'
      profit_dic['bips'] = '--'

  for k in profit_dic.keys():
      if not profit_dic[k]:
          profit_dic[k] = '--'

  if Growthdata.objects.filter(code=code).exists():
      g_result = Growthdata.objects.filter(code=code)
      growth_dic['mbrg'] = g_result[0].mbrg
      growth_dic['nprg'] = g_result[0].nprg
      growth_dic['nav'] = g_result[0].nav
      growth_dic['targ'] = g_result[0].targ
      growth_dic['epsg'] = g_result[0].epsg
      growth_dic['seg'] = g_result[0].seg

  else:
     growth_dic['mbrg'] = '--'
     growth_dic['nprg'] = '--'
     growth_dic['nav'] = '--'
     growth_dic['targ'] = '--'
     growth_dic['epsg'] = '--'
     growth_dic['seg'] = '--'

  for k in growth_dic.keys():
      if not growth_dic[k]:
          growth_dic[k] = '--'
  stock['growth_dic'] = growth_dic
  stock['profit_dic'] = profit_dic
  stock['report_dic'] = report_dic
  stock['basic_dic'] = basic_dic
  return render(request,'finweb/fin_data.html',{'stock':stock})

def notices(request):
  code = request.session.get('code')
  query = Stockdata.objects.filter(code=code)
  name = query[0].name
  stock = {}
  stock['code'] = code
  stock['name'] = name
  # print code
  # print "*********\n"
  # print type(code)
  a = ts.get_notices(str(code))[:10]
  # print "error here??"
  notices = []
  for i in range(10):
      dic = {}
      dic['type'] = a.ix[i]['type']
      dic['title']=a.ix[i]['title']
      dic['date']=a.ix[i]['date']
      dic['url']=a.ix[i]['url']
      notices.append(dic)
  stock['notices'] = notices
  return render(request,'finweb/notices.html',{'stock':stock})

def quant(request):
    portfolio_list = []
    user = User.objects.get(username=request.user.username)
    port = Portfolio.objects.filter(user_id=user.id)
    for p in port:
        dic = {}
        dic['name'] = p.name
        portfolio_list.append(dic)
    return render(request,'finweb/quant.html',{'portfolio_list':portfolio_list})

def get_quant_data(request):
    # item.name close item.pb item.pcf  item.profits_yoy item.targ item.nav item.mbrg item.nprg item.epsg
    user = User.objects.get(username=request.user.username)
    p_name = request.GET.get('port_name','')
    portfolio = Portfolio.objects.get(name= p_name,user_id=user.id)
    stock_list = str(portfolio.list).split(';')
    if stock_list and stock_list[0]=='':
          request.session['p_name'] = p_name
          print "*******",p_name
          quant_list = []
          return JsonResponse(quant_list,safe=False)
    quant_list = []
    request.session['p_name'] = p_name
    for stock in stock_list:
        dic = {}
        data =ts.get_realtime_quotes(stock)
        dic['name'] =data.ix[0]['name']
        dic['close'] = round(float(data.ix[0]['pre_close']),2)
        # print dic['close']
        if Stockdata.objects.filter(code=stock).exists():
            s_result = Stockdata.objects.filter(code = stock)
            dic['pb']= s_result[0].pb
            # print "****************************",dic['pb']
        else:
            dic['pb'] = '--'
        if Reportdata.objects.filter(code=stock).exists():

            r_result = Reportdata.objects.filter(code=stock)
            # epcf = r_result[0].epcf
            # print epcf
            # dic['pcf'] = dic['close']/float(epcf)
            # print dic['pcf']
            dic['profits_yoy'] = r_result[0].profits_yoy
            # print dic['profits_yoy']
        else:
            dic['pcf'] = '--'
            dic['profits_yoy'] = '--'
        if Growthdata.objects.filter(code=stock).exists():
            g_result = Growthdata.objects.filter(code=stock)
            dic['targ'] = g_result[0].targ
            dic['nav'] = g_result[0].nav
            dic['mbrg'] = g_result[0].mbrg
            dic['nprg'] = g_result[0].nprg
            dic['epsg'] = g_result[0].epsg
        else:

            dic['targ'] = '--'
            dic['nav'] = '--'
            dic['mbrg'] = '--'
            dic['nprg'] = '--'
            dic['epsg'] = '--'

        for k in dic.keys():
            if (not dic[k]) or dic[k]=='--':
                 break
        else:
            quant_list.append(dic)
    # print quant_list
    # print "*********************************************"
    return JsonResponse(quant_list,safe=False)

def factor_analysis(request):
    user = User.objects.get(username=request.user.username)
    port = Portfolio.objects.filter(user_id=user.id)
    cur_p = request.session.get('p_name',port[0].name)
    portfolio = Portfolio.objects.get(name= cur_p,user_id=user.id)
    stock_list = str(portfolio.list).split(';')
    flag = False
    if stock_list and stock_list[0]=='':
        flag = True
        # dic = {}
        # dic['code'] = u'组合中没有股票'
        # dic['name'] = '--'
        # dic['name']='--'
        # dic['close'] = '--'
        # dic['pb'] = '--'
        # dic['pcf'] = '--'
        # dic['profits_yoy'] = '--'
        # dic['targ'] = '--'
        # dic['nav'] = '--'
        # dic['mbrg'] = '--'
        # dic['nprg'] = '--'
        # dic['epsg'] = '--'
        # sort_list = []
        # sort_list.append(dic)
        # return render(request,'finweb/factor_analysis.html',{'sort_list':sort_list,'p_name':cur_p})
        return render(request,'finweb/factor_analysis.html',{'p_name':cur_p,'flag':flag})
    quant_list = []
    for stock in stock_list:
        dic = {}
        data =ts.get_realtime_quotes(stock)
        dic['code'] = stock
        dic['name'] =data.ix[0]['name']
        dic['close'] = round(float(data.ix[0]['pre_close']),2)
        if Stockdata.objects.filter(code=stock).exists():
            s_result = Stockdata.objects.filter(code = stock)
            dic['pb']= s_result[0].pb
        else:
            dic['pb'] = '--'
        if Reportdata.objects.filter(code=stock).exists():
            r_result = Reportdata.objects.filter(code=stock)
            dic['profits_yoy'] = r_result[0].profits_yoy
        else:
            dic['pcf'] = '--'
            dic['profits_yoy'] = '--'
        if Growthdata.objects.filter(code=stock).exists():
            g_result = Growthdata.objects.filter(code=stock)
            dic['targ'] = g_result[0].targ
            dic['nav'] = g_result[0].nav
            dic['mbrg'] = g_result[0].mbrg
            dic['nprg'] = g_result[0].nprg
            dic['epsg'] = g_result[0].epsg
        else:

            dic['targ'] = '--'
            dic['nav'] = '--'
            dic['mbrg'] = '--'
            dic['nprg'] = '--'
            dic['epsg'] = '--'

        for k in dic.keys():
            if (not dic[k]) or dic[k]=='--':
                 break
        else:
            quant_list.append(dic)

    sort_list = []
    for dic in quant_list:
        factor_dic = {}
        factor_dic['code'] = dic['code']
        factor_dic['name'] = dic['name']
        factor_dic['close'] = dic['close']
         # item.pb  item.profits_yoy item.targ item.nav item.mbrg item.nprg item.epsg
        mark = float(dic['pb'])*(-0.1109)+float(dic['profits_yoy'])*(0.2215)+float(dic['targ'])*(0.0889)+float(dic['nav'])*(0.0954)+float(dic['mbrg'])*(0.0621)+float(dic['nprg'])*(0.1547)+float(dic['epsg'])*(0.1173)
        factor_dic['mark'] = mark
        sort_list.append(factor_dic)
    sort_list.sort(key=lambda x:x['mark'],reverse=True)
    return render(request,'finweb/factor_analysis.html',{'sort_list':sort_list,'p_name':cur_p,'flag':flag})

def stock_ratio(request):
    user = User.objects.get(username=request.user.username)
    port = Portfolio.objects.filter(user_id=user.id)
    p_name = request.session.get('p_name',port[0].name)

    return render(request,'finweb/stock_ratio.html',{'p_name':p_name})

def get_stock_ratio(request):
    user = User.objects.get(username=request.user.username)
    port = Portfolio.objects.filter(user_id=user.id)
    cur_p = request.session.get('p_name',port[0].name)
    print "***********",cur_p
    portfolio = Portfolio.objects.get(name= cur_p,user_id=user.id)
    stock_list = str(portfolio.list).split(';')
    print "**********",stock_list
    dic = {}
    #部分股票timetomarket，不再所选时间范围内的情况
    start = request.GET.get('from')
    end = request.GET.get('to')
    print "**********",start,end,type(start)
    close_list = []
    name_list = []
    for stock in stock_list:
        data = ts.get_k_data(stock,start = start, end = end)
        d = data.loc[:,['date','close']]
        close = d.set_index('date')
        close.columns = [stock]
        close_list.append(close)
        name = Stockdata.objects.filter(code = stock)[0].name
        name_list.append(name)
    print "**********",name_list,close_list
    result = pd.concat(close_list, axis=1, join='inner')
    print "**********",result
    price_list = list(result.ix[0])
    print "**********",price_list
    days = len(result)
    noa = len(stock_list)
    returns = np.log(result/result.shift(1))
    def statistics(weights):
         weights = np.array(weights)
         port_returns = np.sum(returns.mean()*weights)*days
         port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*days,weights)))
         return np.array([port_returns, port_variance, port_returns/port_variance])
    def min_sharpe(weights):
         return -statistics(weights)[2]
    cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1})
    bnds = tuple((0,1) for x in range(noa))
    #优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测),使用平均分布。
    print  "**********  opts\n"
    opts = sco.minimize(min_sharpe, noa*[1./noa,], method = 'SLSQP', bounds = bnds, constraints = cons)
    print opts
    #最大夏普指数
    print "to_list_before"
    sharpe_ratio = opts['x'].round(3).tolist()
    print "to_list_after"
    #预期收益率，预期波动率，最优夏普指数
    sharpe_result = statistics(opts['x']).round(3).tolist()
    print "*********",sharpe_result,sharpe_ratio
    def min_variance(weights):
        return statistics(weights)[1]
    optv = sco.minimize(min_variance, noa*[1./noa,],method = 'SLSQP', bounds = bnds, constraints = cons)
    print "********",optv
    #最小方差
    variance_ratio = optv['x'].round(3).tolist()
    #预期收益率，预期波动率，夏普指数
    variance_result = statistics(optv['x']).round(3).tolist()
    print "*********",variance_result,variance_ratio
    #还要返回每只股票的初始价格
    returns_mat = returns[1:].as_matrix(columns=None)
    sharpe_ret = np.dot(returns_mat,opts['x'].round(3))
    variance_ret = np.dot(returns_mat,optv['x'].round(3))
    dates = np.array(returns.index[1:])
    returns_dataframe = pd.DataFrame(np.vstack((dates,sharpe_ret,variance_ret)).T)
    return_str = returns_dataframe.to_json(orient="values")
    result_dic = {}
    result_dic['price_list'] = price_list
    result_dic['sharpe_ratio'] = sharpe_ratio
    result_dic['sharpe_result'] = sharpe_result
    result_dic['variance_ratio'] = variance_ratio
    result_dic['variance_result'] = variance_result
    result_dic['stock_list'] = stock_list
    result_dic['name_list'] = name_list
    result_dic['return_str'] = return_str
    return JsonResponse(result_dic,safe=False)


def revenue_test(request):
    return HttpResponse("Nothing Yet");


def candle1(request):
    return render(request,'finweb/candle_test.html',{})

def news_test(request):
    a = ts.get_latest_news(top= 6 ,show_content=True)
    news_list1 = []
    news_list2 = []
    for i in range(3):
        dic1 = {}
        dic1['classify'] = a.ix[i]['classify']
        dic1['title']=a.ix[i]['title']
        dic1['time']=a.ix[i]['time']
        dic1['url']=a.ix[i]['url']
        dic1['content']=a.ix[i]['content'][0:100]+"....."
        dic2 = {}
        dic2['classify'] = a.ix[i+3]['classify']
        dic2['title']=a.ix[i+3]['title']
        dic2['time']=a.ix[i+3]['time']
        dic2['url']=a.ix[i+3]['url']
        dic2['content']=a.ix[i+3]['content'][0:100]+"....."
        news_list1.append(dic1)
        news_list2.append(dic2)
    return render(request,'finweb/news_test.html',{'news_list1':news_list1,'news_list2':news_list2})

def candle(request):
    return render(request,'finweb/candle_test.html',{})

def echarts(request):
    index1 = request.GET.get('index')
    print "we are in echarts!\n"
    print index1
    dic = {'categories':["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"],'data': [5, 20, 36, 10, 10, 20]}
    return JsonResponse(dic,safe=False)

def test(request):
    return render(request,'finweb/test.html',{})



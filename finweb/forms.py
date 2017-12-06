# -*- coding: utf-8 -*-
from django import forms
from finweb.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

class UserForm(forms.ModelForm):
    username = forms.CharField(error_messages={'required':u'用户名不能为空'})
    email = forms.EmailField(error_messages={'required':u'邮箱不能为空','invalid':u'请输入正确的邮箱'})
    password = forms.CharField(min_length=6,error_messages={'required':u'用户名不能为空','min_length':u'至少输入6位密码'})
    def clean(self):
        cleaned_data = self.cleaned_data
        data_username = cleaned_data.get('username')
        data_email = cleaned_data.get('email')
        if data_username:
            username_exist = User.objects.filter(username= data_username).exists()
            if username_exist:
                raise forms.ValidationError(u'用户名已经存在，请更换')
        if data_email:
            email_exist = User.objects.filter(email = data_email).exists()
            if email_exist:
                raise forms.ValidationError(u'邮箱已经注册，请直接登录')
    class Meta:
        model = User
        fields = ('username','email','password')


class UserProfileForm(forms.ModelForm):
    phonenum =forms.CharField(error_messages={'required':u'电话号码不能为空','invalid':'长度超出限制'})
    birthday =forms.DateField(input_formats=['%Y-%m-%d',],error_messages={'required':u'请填写生日信息','invalid':'请按照正确的格式填写生日'})
    class Meta:
        model = UserProfile
        fields = ('gender','phonenum','birthday')

class LoginForm(forms.ModelForm):
    username = forms.CharField(error_messages={'required':u'用户名不能为空'})
    password = forms.CharField(min_length=6,error_messages={'required':u'密码不能为空'})
    def clean(self):
        cleaned_data = self.cleaned_data
        data_username = cleaned_data.get('username')
        data_password = cleaned_data.get('password')
        if data_password:
            user = authenticate(username=data_username,password=data_password)
            if not user:
                print data_username,data_password
                raise forms.ValidationError(u"用户名或密码错误")
        return cleaned_data
    class Meta:
        model = User
        fields = ('username','password')

# class changeinfoForm(forms.ModelForm):
#     username = forms.CharField(error_messages={'required':u'用户名不能为空'})
#     # def clean(self):
#     #     cleaned_data = self.cleaned_data
#     #     data_username = cleaned_data.get('username')
#     #     if data_username:
#     #         username_exist = User.objects.filter(username= data_username).exists()
#     #         if username_exist:
#     #             raise forms.ValidationError(u'用户名已经存在，请更换')
#     class Meta:
#         model = User
#         fields = ('username',)

class changepasswordForm(forms.ModelForm):
    oldpassword = forms.CharField(min_length=6,error_messages={'required':u'密码不能为空'})
    password = forms.CharField(min_length=6,error_messages={'required':u'密码不能为空','min_length':u'至少输入6位密码'})
    password_again = forms.CharField(min_length=6,error_messages={'required':u'密码不能为空','min_length':u'至少输入6位密码'})
    def clean(self):
        cleaned_data = self.cleaned_data
        data_password = cleaned_data.get('password')
        data_password_again = cleaned_data.get('password_again')
        if data_password != data_password_again:
            raise forms.ValidationError(u"两次输入的新密码不一致！")
        return cleaned_data
    class Meta:
        model = User
        fields = ('password',)



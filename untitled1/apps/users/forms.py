_auther_ = 'Harry'
_date_ = '2/1/2018 12:31 AM'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True) # null 则报错   并且username必须和前端的要验证的name一样
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"please input correctly"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":"please input correctly"})


class ModifyPwdForm(forms.Form):

    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # 指明来自于哪个model
        fields = ['image']  # 挑出自己需要的字段\



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # 指明来自于哪个model
        fields = ['nick_name','gender','birday','address','mobile']  # 挑出自己需要的字段\
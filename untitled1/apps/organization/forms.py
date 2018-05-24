_auther_ = 'Harry'
_date_ = '2/6/2018 9:25 PM'

from django import forms
from operation.models import UserAsk
import re #正则表达式


#用户咨询表单
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone = forms.CharField(required=True,min_length=10,max_length=14)
#     course_name = forms.CharField(required=True,min_length=5,max_length=50)
#
#     #不难发现这个class和我们在operation中定义的非常相似，再重写一遍是非常浪费时间的，所以才有了 modelform


class UserAskForm(forms.ModelForm):
    # 继承之余还可以新增字段

    class Meta:
        model = UserAsk   #指明来自于哪个model
        fields=['name','mobile','course_name'] #挑出自己需要的字段\

    def clean_mobile(self): #验证手机号码是否合法
        mobile=self.cleaned_data['mobile']  #当提交一个form以后，将被清除的数据放到了 cleaned_data里面
        REGER_MOBILE ="^1[358]\d{9}$|^147\d{8}$|^176\d{8}|^226\d{7}$"
        p = re.compile(REGER_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("your phone number invalid",code="mobile_invalidation")





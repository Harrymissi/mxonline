from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser   #可以继承自动生成的user表里的属性
# Create your models here.

# 自己添加需要的属性


class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50,verbose_name="nickname",default="")
    birday=models.DateField(verbose_name="birthday",null=True,blank=True)
    gender=models.CharField(choices=(("male","male"),("female","female")),default="",max_length=10)
    address=models.CharField(max_length=100,default="")
    mobile=models.CharField(max_length=11,null=True,blank=True)
    image=models.ImageField(upload_to="image/%Y/%m",default="image/default.png",max_length=100) #头像
    email = models.CharField(max_length=50,verbose_name="email",default="")

    class Meta:
        verbose_name="user profile"   #在model中的名称
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self): # 获取用户未读消息的数量
        from operation.models import UserMessage
        return  UserMessage.objects.filter(user=self.id,has_read=False).count()



class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=20, verbose_name="verifycode")
    email=models.EmailField(max_length=50, verbose_name="email")
    send_type=models.CharField(choices=(("register","register"),("forget","forget"),("update_email","update email")),max_length=20,verbose_name='sending type')
    send_time=models.DateTimeField(default=datetime.now,verbose_name='sending time')

    class Meta:
        verbose_name="email verifycode"
        verbose_name_plural=verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name="title")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name="banner images")
    url = models.URLField(max_length=200, verbose_name="url")
    index = models.IntegerField(default=100, verbose_name="order") #播放顺序
    add_time=models.DateTimeField(default=datetime.now,verbose_name="add_time")

    class Meta:
        verbose_name="banner"
        verbose_name_plural=verbose_name
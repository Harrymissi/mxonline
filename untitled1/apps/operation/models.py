from django.db import models

from datetime import  datetime

from users.models import UserProfile
from courses.models import Course       # 做外键使用


# Create your models here.

class UserAsk(models.Model):
    name=models.CharField(max_length=20,verbose_name="user_name")
    mobile=models.CharField(max_length=11,verbose_name="phone")
    course_name=models.CharField(max_length=50,verbose_name="course_name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name="user_ask"
        verbose_name_plural=verbose_name

class CourseComments(models.Model):
    user=models.ForeignKey(UserProfile,verbose_name="user",on_delete=models.CASCADE)
    course=models.ForeignKey(Course,verbose_name="course",on_delete=models.CASCADE)
    comment=models.CharField(max_length=200, verbose_name="comment")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name="course_comment"
        verbose_name_plural=verbose_name

class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user",on_delete=models.CASCADE) #用户的收藏有 机构/课程/教师
    fav_id=models.IntegerField(default=0,verbose_name="fav_id")
    fav_type=models.IntegerField(choices=((1,"course"),(2,"org"),(3,"teacher")),default=1,verbose_name="fav_type")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name="user_fav"
        verbose_name_plural=verbose_name

class UserMessage(models.Model):
    user=models.IntegerField(default=0, verbose_name="accept_user") #若为0的话是给所有用户发消息
    message = models.CharField(max_length=500, verbose_name= "message_content")
    has_read = models.BooleanField(default=False, verbose_name="has_read")  #在做bool类型的时候命名规则是has_.....
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name="user_message"
        verbose_name_plural=verbose_name

class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user",on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="course",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")

    class Meta:
        verbose_name="user_course"
        verbose_name_plural=verbose_name








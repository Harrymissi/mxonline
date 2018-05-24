_auther_ = 'Harry'
_date_ = '2/27/2018 11:42 PM'

from django.urls import path, re_path
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView


app_name="users"
urlpatterns=[
   path('info/', UserInfoView.as_view(),name="user_info"), #用户信息
   path('image/upload/', UploadImageView.as_view(), name="image_upload"), #用户头像上传
   path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),# 用户中心修改密码
   path('sendemail_code/', SendEmailCodeView.as_view(), name="update_email"), # 发送验证码
   path('update_email/', UpdateEmailView.as_view(), name="update_email"), # 用户中心修改邮箱
   path('mycourses/', MyCourseView.as_view(),name="mycourses"),   #用户参加了的课程
   path('myfav/org/', MyFavOrgView.as_view(),name="myfav_org"),  #用户收藏的机构
   path('myfav/teacher/',MyFavTeacherView.as_view(),name="myfav_teacher"),  #用户收藏的教师
   path('myfav/course/',MyFavCourseView.as_view(),name="myfav_course"),  #用户收藏的课程
   path('mymessage/',MyMessageView.as_view(),name="my_message"),  #我的消息
        ]
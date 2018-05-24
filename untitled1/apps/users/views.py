from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout  #认证
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from django.db.models import  Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm , ForgetForm , ModifyPwdForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from .utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
import json
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try :
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class  ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return  render(request,'login.html')




class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")  # 取不到时候为空  username和password是前端页面账号名密码的name
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{"register_form":register_form,"msg":"user exist!"})
            user_psw = request.POST.get("password", "")
            user_profile=UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password=make_password(user_psw)
            user_profile.save()

            # 生成 “欢迎注册” 消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "welcome sign up "
            user_message.save()

            send_register_email(user_name,"register")
            return render(request, 'login.html ')
        else:
            return render(request,'register.html',{"register_form":register_form})





class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))  # 提供个url给reverse函数反解成地址跳转





class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): # 验证用户名或密码是否为空
            user_name = request.POST.get("username", "")  # 取不到时候为空  username和password是前端页面账号名密码的name
            user_psw = request.POST.get("password", "")
            user = authenticate(username=user_name, password=user_psw)  # 成功返回user对象,失败返回null
            if user is not None:  # 如果不是null说明验证成功
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", {})  # 登陆成功跳回首页
                else:
                    return render(request, "login.html",
                                  {"msg": "your account is not activated"})

            else :
                return render(request, "login.html",
                              {"msg": "username or password is wrong"})
        else:
            return render(request, "login.html", {"login_form":login_form})



# def user_login(request):
#     if request.method=='POST':
#         user_name=request.POST.get("username","")    # 取不到时候为空  username和password是前端页面账号名密码的name
#         user_psw = request.POST.get("password", "")
#
#         user=authenticate(username=user_name,password=user_psw)    #成功返回user对象,失败返回null
#         if user is not None:        # 如果不是null说明验证成功
#
#             login(request,user)
#             # login 两参数：request, user
#             # 实际是对request写了一部分东西进去，然后在render的时候：
#             # request是要render回去的。这些信息也就随着返回浏览器。完成登录
#             # 跳转到首页 user request会被带回到首页
#
#             return render(request,"index.html",{}) #登陆成功跳回首页
#         else:
#             return render(request,"login.html",{"msg":"username or password is wrong"})
#
#
#     elif request.method=="GET":
#         return render(request,"login.html",{})

class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetForm()
        return  render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")              #如果验证成功 ....
            return  render(request,"login.html.html")
        else:
            return  render(request,'forgetpwd.html',{'forget_form':forget_form})



class  ResetView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request, 'active_fail.html')
        return  render(request,'login.html')



class ModifyPwdView(View):
    def post(self,request):
        modify_form =  ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password1","")
            pwd2=request.POST.get("password2","")
            email=request.POST.get("email","")
            if pwd1!=pwd2:
                return render(request,"password_reset.html",{"email":email,"msg":"password not same"})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email=request.POST.get("email","")
            return  render(request,"password_reset.html",{"email":email, "modify_form":modify_form})


class UserInfoView(LoginRequiredMixin,View):  #用户个人信息  所以必须登陆才可以访问
    def get(self,request):
        return  render(request,"usercenter-info.html",{
        })

    def post(self, request):
        # 不像用户咨询是一个新的。需要指明instance。不然无法修改，而是新增用户
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return HttpResponse(
                json.dumps(
                    user_info_form.errors),
                content_type='application/json')




class UploadImageView(LoginRequiredMixin,View):   #用户修改头像
    def post(self,request):
        image_forms = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_forms.is_valid():
            request.user.save()
            return  HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')



class UpdatePwdView(View):
    def post(self,request):
        modify_form =  ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password1","")
            pwd2=request.POST.get("password2","")

            if pwd1!=pwd2:
                return HttpResponse('{"status":"fail","msg":"two password not same"}', content_type='application/json')
            user = request.user
            user.password=make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:

            return  HttpResponse(json.dumps(modify_form.errors), content_type='application/json')



class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        # 取出需要发送的邮件
        email = request.GET.get("email", "")

        # 不能是已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                '{"email":"邮箱已经存在"}',
                content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse(
            '{"status":"success"}',
            content_type='application/json')




class UpdateEmailView(LoginRequiredMixin,View): # 修改个人邮箱
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_record = EmailVerifyRecord.objects.filter(email = email, code = code, send_type = "update_email")
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"verify code is wrong"}', content_type='application/json')




class MyCourseView(LoginRequiredMixin,View): #我的课程
    def get(self,request):
        user_courses = UserCourse.objects.filter(user = request.user)
        return render(request,'usercenter-mycourse.html',{
            "user_courses":user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):  # 我收藏的机构
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id  # 获得机构 id
            org = CourseOrg.objects.get(id = org_id)
            org_list.append(org)   # 把这些机构放到一个 list 中

        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):  # 我收藏的教师
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id  # 获得机构 id
            teacher = Teacher.objects.get(id = teacher_id)
            teacher_list.append(teacher)   # 把这些机构放到一个 list 中

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):  # 我收藏的教师
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id  # 获得机构 id
            course = Course.objects.get(id = course_id)
            course_list.append(course)   # 把这些机构放到一个 list 中

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })



class MyMessageView(LoginRequiredMixin,View):  #我的消息
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)
         # 用户进入个人消息后清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(has_read=False,user= request.user.id)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()



        try:  #对个人消息进行分页
              #  尝试获取前台get请求传递过来的page参数
              # 如果是不合法的配置参数默认返回第一页

            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message,5,request=request)
        messages = p.page(page)

        return render(request,"usercenter-message.html",{
            "messages":messages,

        })



class IndexView(View):  # 首页
    def get(self,request):

        #取出轮播图
        all_banner = Banner.objects.all().order_by('index')

        #取出课程
        course = Course.objects.filter(is_banner=False)[:5] # 取五个当普通的展示
        banner_course = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()

        return render(request,"index.html",{
            'all_banner':all_banner,
            'courses': course,
            'banner_courses': banner_course,
            'course_orgs' : course_orgs

        })








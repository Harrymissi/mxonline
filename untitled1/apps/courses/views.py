from django.shortcuts import render
from django.views.generic.base import View
from .models import Course,CourseResource,Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments,UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import  Q
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_course = Course.objects.all().order_by("-add_time") #因为默认是以最新排序
        hot_courses = Course.objects.all().order_by("-fav_nums")[0:3]

        search_keywords = request.GET.get('keywords',"")  #课程搜索
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) |Q(desc__icontains=search_keywords)|Q(details__icontains=search_keywords)) #类似于sql的like语句,不区分大小写

        # 排序
        sort = request.GET.get('sort', '')
        if sort == 'students':  # 从前台取出的sort==students
            all_course = all_course.order_by('-student')  # 括号里的字段必须和数据库里的一致
        elif sort == 'hot':
            all_course = all_course.order_by('-click_num')  #根据点击数量来算


        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 3, request=request)  # 这里指从all_org中取3个出来，每页显示3个
        courses = p.page(page)



        return render(request,'course-list.html',{
            "all_course":courses,
            "sort":sort,
            "hot_courses":hot_courses,


        })


class CourseDetailView(View):
    #课程详情页
   def get(self,request,course_id):
       course = Course.objects.get(id=int(course_id))

       #查看课程详情就是增加了课程点击数
       course.click_num+=1
       course.save()

       has_fav_course = False
       has_fav_org = False

       if request.user.is_authenticated:
           if UserFavorite.objects.filter(user = request.user, fav_id=course.id, fav_type=1):
               has_fav_course = True
           if UserFavorite.objects.filter(user = request.user, fav_id=course.course_org.id, fav_type=2):
               has_fav_org = True


       tag = course.tag
       if tag:
           relate_course = Course.objects.filter(tag = tag)[1:2]  #取一个tag相同的课程出来,从1开始否则推荐自己
       else:
           relate_course = []   #怕万一tag为空的话 html页面会报错

       return  render(request,'course-detail.html',{
           "course":course,
           "relate_courses":relate_course,
           "has_fav_course":has_fav_course,
           "has_fav_org":has_fav_org,


       })


class CourseInfoView(LoginRequiredMixin,View):
    #课程章节信息

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))   #获取课程

        course.student +=1 # 每次点击是执行的课程信息页面，点击数加一
        course.save()

        #查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user = request.user, course = course)
        if not user_courses:  #如果不存在
            user_course = UserCourse(user = request.user, course = course) #更新用户与课程关联
            user_course.save()

        user_courses = UserCourse.objects.filter(course = course) # 选出学了这门课的学生关系
        user_ids = [user_course.user.id for user_course in user_courses]   # 从关系中取出user_id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)    #user是个外键，直接加下划线id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]   #取出所有课程id
        relate_courses= Course.objects.filter(id__in=course_ids).order_by("-click_num").exclude(id =course.id)[:4]  #根据点击量进行排序， 取五个
        # 获取学过该课程用户学过的其他课程
        #逻辑： 获取当前课程id，查出所有学了该科的用户，遍历这些用户学过哪些课程，再按点击率进行排序


        all_resources = CourseResource.objects.filter(course = course)



        return  render(request,"course-video.html",{
            "course":course,
            "course_resources":all_resources,
            "relate_courses":relate_courses,
        })



class CommentsView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))   #获取课程
        all_resources = CourseResource.objects.filter(course = course)
        all_comment = CourseComments.objects.all()
        all_resources = CourseResource.objects.filter(course=course)
        return render(request,"course-comment.html",{
            "all_comments":all_comment,
            "course":course,
            "course_resources": all_resources,

        })

class AddCommentsView(View):  #用户添加评论
    def post(self,request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments", "")

        if int(course_id) >0 and comments:    #  判断传回来的值是否有效  id>0 且 评论不能为空
            course_comments = CourseComments()
            course = Course.objects.get(id = int(course_id))
            # get只能取出一条数据，如果有多条抛出异常。没有数据也抛异常
            # filter取一个列表出来，queryset。没有数据返回空的queryset不会抛异常
            course_comments.course = course
            course_comments.user = request.user
            course_comments.comment = comments
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')



class VideoPlayView(View):

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))   #获取课程
        course = video.lesson.course

        #查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user = request.user, course = course)
        if not user_courses:  #如果不存在
            user_course = UserCourse(user = request.user, course = course) #更新用户与课程关联
            user_course.save()

        user_courses = UserCourse.objects.filter(course = course) # 选出学了这门课的学生关系
        user_ids = [user_course.user.id for user_course in user_courses]   # 从关系中取出user_id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)    #user是个外键，直接加下划线id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]   #取出所有课程id
        relate_courses= Course.objects.filter(id__in=course_ids).order_by("-click_num").exclude(id =course.id)[:4]  #根据点击量进行排序， 取五个
        # 获取学过该课程用户学过的其他课程
        #逻辑： 获取当前课程id，查出所有学了该科的用户，遍历这些用户学过哪些课程，再按点击率进行排序


        all_resources = CourseResource.objects.filter(course = course)



        return  render(request,"course-play.html",{
            "course":course,
            "course_resources":all_resources,
            "relate_courses":relate_courses,
            "video":video,
        })







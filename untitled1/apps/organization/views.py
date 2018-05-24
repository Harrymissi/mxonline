from django.shortcuts import render
from django.views.generic import  View
from .models import CourseOrg,CityDict,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from courses.models import Course
from operation.models import UserFavorite
from django.db.models import  Q
# Create your views here.

class OrgView(View):    #课程机构列表
    def get(self,request):
        all_orgs=CourseOrg.objects.all()

        all_citys=CityDict.objects.all()

        # 热门机构,如果不加负号会是有小到大，取三个
        hot_orgs=all_orgs.order_by("-click_nums")[:3]

        #取出筛选城市
        city_id=request.GET.get('city','')
        if city_id:
            #外键city再数据库中叫city_id
            all_orgs=all_orgs.filter(city_id=int(city_id))


        #类别筛选
        category = request.GET.get('ct', '')
        if category:
            # 外键city再数据库中叫city_id
            all_orgs = all_orgs.filter(category=category)

        #进行排序
        sort=request.GET.get('sort','')
        if sort=='students':  #从前台取出的sort==students
            all_orgs=all_orgs.order_by('-students')   #括号里的字段必须和数据库里的一致
        elif sort=='courses':
            all_orgs=all_orgs.order_by('-course_nums')


        org_nums = all_orgs.count() #机构数量统计



        search_keywords = request.GET.get('keywords',"")  #机构搜索
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |Q(desc__icontains=search_keywords))


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)    # 这里指从all_org中取3个出来，每页显示3个
        orgs = p.page(page)


        return  render(request,'org-list.html',{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        })


class AddUserAskView(View):
    #提交表单大多数做post请求

        def post(self,request):
            userask_form = UserAskForm(request.POST)
            if userask_form.is_valid():
                # 这里是modelform和form的区别
                # 它有model的属性
                # 当commit为true进行真正保存
                user_ask = userask_form.save(commit=True)
                # 这样就不需要把一个一个字段取出来然后存到model的对象中之后save

                # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的是json,
                return HttpResponse('{"status":"success"}',content_type='application/json')
            else:
                # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
                return HttpResponse('{"status":"fail", "msg":"please check what u input"}', content_type='application/json')



class OrgHomeView(View):  #机构首页

    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()

        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()[:3]   #取三个
        all_teachers = course_org.teacher_set.all()[:2]

        return  render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav

        })


class OrgCourseView(View):  #机构课程

    def get(self,request,org_id):
        current_page="course"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()


        return  render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,    #用来判断左边栏中选中了哪个
            'has_fav':has_fav


        })



class OrgDescView(View):  #机构详情

    def get(self,request,org_id):
        current_page="desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return  render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,    #用来判断左边栏中选中了哪个
            'has_fav':has_fav,

        })



class OrgTeahcherView(View):  #机构老师

    def get(self,request,org_id):
        current_page="course"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_teachers = course_org.teacher_set.all()


        return  render(request,'org-detail-teachers.html',{
            'all_teacher':all_teachers,
            'course_org':course_org,
            'current_page':current_page,    #用来判断左边栏中选中了哪个
            'has_fav':has_fav

        })


class AddFavView(View):
    """
    用户收藏与取消收藏功能
    """
    def post(self, request):
        # 表明你收藏的不管是课程，讲师，还是机构。他们的id
        # 默认值取0是因为空串转int报错
        id = request.POST.get('fav_id', 0)
        # 取到你收藏的类别，从前台提交的ajax请求中取
        type = request.POST.get('fav_type', 0)

        # 收藏与已收藏取消收藏
        # 判断用户是否登录:即使没登录会有一个匿名的user
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"user not login"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()

            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -=1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -=1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"add "}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 过滤掉未取到fav_id type的默认情况
            if int(type) >0 and int(id) >0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"added "}', content_type='application/json') #添加成功
            else:
                return HttpResponse('{"status":"fail", "msg":"added failed"}', content_type='application/json')#添加失败


class TeacherListView(View):
    # 课程讲师列表页
    def get(self,request):
        all_teachers = Teacher.objects.all() #取到所有的教师

        search_keywords = request.GET.get('keywords', "")  # 机构搜索
        if search_keywords:
            all_teachers= all_teachers.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords)|Q(work_position__icontains=search_keywords))



        sort = request.GET.get('sort',"")
        if sort:
            if sort == "hot":  #按人气排序
                all_teachers = all_teachers.order_by("-fav_nums")


        sorted_teacher = Teacher.objects.all().order_by("-fav_nums")


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)  # 这里指从all_org中取3个出来，每页显示3个
        teachers = p.page(page)


        return  render(request,"teachers-list.html",{
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,

        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        teacher.click_nums +=1
        teacher.save()
        all_courses = Course.objects.filter(teacher = teacher)

        sorted_teacher = Teacher.objects.all().order_by("-fav_nums")

        has_teacher_fav = False
        if UserFavorite.objects.filter(user = request.user,fav_type=3,fav_id=teacher.id):
            has_teacher_fav = True

        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_fav = True

        return  render(request,"teacher-detail.html",{
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teacher": sorted_teacher,
            "has_teacher_fav":has_teacher_fav,
            "has_org_fav":has_org_fav
        })







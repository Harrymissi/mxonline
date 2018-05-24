_auther_ = 'Harry'
_date_ = '2/6/2018 9:37 PM'


from django.urls import path, include , re_path
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeahcherView,AddFavView,TeacherListView,TeacherDetailView

app_name="organization" #解决2.0.1的报错

urlpatterns=[
    #课程机构列表页, 在app下创建urls文件就是为了防止随着project的越来越大，根目录的urls会越来越臃肿，如果在app下配置好了urls，我们只需要在project下的urls中include进来即可！

    path('list/', OrgView.as_view(),name="org_list"), #那么访问它 则是 127.0.0.1:8000/org/list
    path('add_ask/',AddUserAskView.as_view(),name="add_ask"),
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),
    re_path('org_teacher/(?P<org_id>\d+)/', OrgTeahcherView.as_view(), name="org_teacher"),

    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),

    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"), #讲师详情页

]
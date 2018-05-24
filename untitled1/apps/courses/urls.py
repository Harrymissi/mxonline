_auther_ = 'Harry'
_date_ = '2/11/2018 10:45 PM'

from django.urls import path, include , re_path
from .views import CourseListView,CourseDetailView,CourseInfoView, CommentsView,AddCommentsView,VideoPlayView

app_name="organization" #解决2.0.1的报错

urlpatterns=[
    #课程机构列表页, 在app下创建urls文件就是为了防止随着project的越来越大，根目录的urls会越来越臃肿，如果在app下配置好了urls，我们只需要在project下的urls中include进来即可！

    path('list/', CourseListView.as_view(),name="course_list"), #那么访问它 则是 127.0.0.1:8000/org/list
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    re_path('comments/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"), #课程评论
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),
    re_path('video/(?P<video_id>\d+)/',VideoPlayView.as_view(), name="video_play"),




]
_auther_ = 'Harry'
_date_ = '1/28/2018 11:15 PM'

from .models import Course,Lesson,Video,CourseResource
import  xadmin

class CourseAdmin(object):
    list_display=['name','desc','details','degree','learn_time','student','fav_nums','image','click_num','add_time']
    search_fields=['name','desc','details','degree','learn_time','student','fav_nums','image','click_num','add_time'] #搜索字段 会加个搜索栏
    list_filter=['name','desc','details','degree','learn_time','student','fav_nums','image','click_num','add_time'] #加了个过滤器

class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name'] #搜索字段 会加个搜索栏
    list_filter=['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']  # 搜索字段 会加个搜索栏
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name','download','add_time']
    search_fields = ['course', 'name','download']  # 搜索字段 会加个搜索栏
    list_filter = ['course', 'name','download','add_time']



xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

_auther_ = 'Harry'
_date_ = '1/29/2018 12:35 AM'

import xadmin
from .models import CourseComments,UserMessage,UserAsk,UserCourse,UserFavorite

class UserAskAdmin(object):
    list_display = ['name', 'mobile','course_name','add_time']
    search_fields = ['name', 'mobile','course_name']  # 搜索字段 会加个搜索栏
    list_filter = ['name', 'mobile','course_name','add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']  # 搜索字段 会加个搜索栏
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course','add_time']
    search_fields = ['user', 'course']  # 搜索字段 会加个搜索栏
    list_filter = ['user', 'course','add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type','add_time']
    search_fields = ['user', 'fav_id', 'fav_type']  # 搜索字段 会加个搜索栏
    list_filter = ['user', 'fav_id', 'fav_type','add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']  # 搜索字段 会加个搜索栏
    list_filter = ['user', 'course', 'comment', 'add_time']

xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
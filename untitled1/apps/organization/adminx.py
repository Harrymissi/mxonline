_auther_ = 'Harry'
_date_ = '1/29/2018 12:26 AM'

from .models import CityDict,CourseOrg,Teacher
import xadmin

class CityDictAdmin(object):
    list_display = ['name','desc', 'add_time']
    search_fields = ['name','desc']  # 搜索字段 会加个搜索栏
    list_filter = ['name','desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'add_time','click_nums','fav_nums','image','address','city']
    search_fields = ['name', 'desc','click_nums','fav_nums','image','address','city']  # 搜索字段 会加个搜索栏
    list_filter = ['name', 'desc', 'add_time','click_nums','fav_nums','image','address','city']


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'features', 'fav_nums', 'add_time']
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position', 'features', 'fav_nums']  # 搜索字段 会加个搜索栏
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position', 'features', 'fav_nums', 'add_time']




xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
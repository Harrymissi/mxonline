_auther_ = 'Harry'
_date_ = '1/27/2018 12:28 PM'

import xadmin
from.models import EmailVerifyRecord
from.models import Banner
from xadmin import views

class BaseSetting(object): # 针对全局theme设置的
    enable_themes=True
    use_bootswatch=True


class GlobalSettings(object):
    site_title="mxonlie administration system"   #修改左上角名称和底角名称
    site_footer="mxonline"
    menu_style="accordion"   #可以让app下的小类收缩起来

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type','send_time'] #搜索字段 会加个搜索栏
    list_filter=['code','email','send_type','send_time'] #加了个过滤器


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']  # 搜索字段 会加个搜索栏
    list_filter = ['title', 'image', 'url', 'index','add_time']  # 加了个过滤器

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting) #注册主题修改功能
xadmin.site.register(views.CommAdminView,GlobalSettings)
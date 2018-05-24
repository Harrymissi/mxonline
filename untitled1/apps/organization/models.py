from django.db import models
from datetime import  datetime
# Create your models here.

class CityDict(models.Model):    #机构所在的城市
    name = models.CharField(max_length=20, verbose_name="city_name")
    add_time=models.DateTimeField(default=datetime.now, verbose_name="add_time")
    desc = models.CharField(max_length=200, verbose_name="city_describe")

    class Meta:
        verbose_name="city"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name=models.CharField(max_length=50, verbose_name="org_name")
    desc=models.TextField(verbose_name="org_describe")
    click_nums=models.IntegerField(default=0,verbose_name="click_num")
    fav_nums = models.IntegerField(default=0, verbose_name="fav_num")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="course_logo", max_length=100)
    address=models.CharField(max_length=150, verbose_name="org_address")
    city=models.ForeignKey(CityDict, verbose_name="org_city",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")
    category=models.CharField(default="colledge",verbose_name="org_category",max_length=20,choices=(("colledge","colledge"),("private","private"),("training orgs","training orgs")))
    students=models.IntegerField(default=0, verbose_name="students_nums")
    course_nums=models.IntegerField(default=0, verbose_name="course_nums")


    class Meta:
        verbose_name="course_org"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def get_teacher_nums(self):  #获取机构的教师数量
        return self.teacher_set.all().count()

class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg, verbose_name="teacher_org",on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="teaher_name")
    work_years=models.IntegerField(default=0, verbose_name="work_year")
    work_company=models.CharField(max_length=50, verbose_name="work_company")
    work_position=models.CharField(max_length=50, verbose_name="work_position")
    features=models.CharField(max_length=50, verbose_name="teaching_features")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_time")
    fav_nums = models.IntegerField(default=0, verbose_name="fav_num")
    click_nums = models.IntegerField(default=0, verbose_name="click_num")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="teacher_img", max_length=100,default='')
    age = models.IntegerField(default=18,verbose_name="age  ")

    class Meta:
        verbose_name="course_teacher"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count() #老师在course表里充当外键，所以可以在自定义方法来获得该老师的课程数

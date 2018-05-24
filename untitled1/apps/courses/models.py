from django.db import models
from datetime import  datetime
from organization.models import CourseOrg,Teacher
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="course_org",null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="course_name")
    desc = models.CharField(max_length=300,verbose_name="course_describe")
    details = models.TextField(verbose_name="course_detail")
    degree = models.CharField(choices=(("cj","beginner"),("zj","intermiddiate"),("gj","advanced")),verbose_name="degree",max_length=10)
    learn_time = models.IntegerField(default=0, verbose_name="learn_time")
    student = models.IntegerField(default=0, verbose_name="student_numbers")
    fav_nums = models.IntegerField(default=0, verbose_name="fav_num")
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name="course_img", max_length=100)
    click_num = models.IntegerField(default=0, verbose_name="click_num")
    add_time= models.DateTimeField(default=datetime.now, verbose_name="add_name")
    category = models.CharField(max_length=200, verbose_name='course_category',default='django development')
    tag = models.CharField(default="", verbose_name="course_tag", max_length=10)
    teacher = models.ForeignKey(Teacher,verbose_name='teacher',blank=True,null=True,on_delete=models.CASCADE)
    youneed_know = models.CharField(max_length=300, verbose_name="youneed_know", default='')
    teacher_tell = models.CharField(max_length=300, verbose_name="teacher_tell_you", default='')
    is_banner = models.BooleanField(default=False,verbose_name="is_banner")

    class Meta:
        verbose_name="courses"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def get_lesson_nums(self):
        return  self.lesson_set.all().count()  #获取课程章节数

    def get_learn_users(self):
        return  self.usercourse_set.all()[:5]   #获取学习该门课的用户

    def get_course_lesson(self):  #获取课程的所有章节
        return self.lesson_set.all()



class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="course",on_delete=models.CASCADE)  #因为course与lesson是一对多的关系，用外键
    name = models.CharField(max_length=100, verbose_name="lesson_name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_name")
    lesson_time = models.IntegerField(default=0, verbose_name="lesson_time")

    class Meta:
        verbose_name="lesson"
        verbose_name_plural=verbose_name

    def __str__(self):
        return  self.name

    def get_lesson_video(self):
        return self.video_set.all()  #获取章节的视频



class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="lesson",on_delete=models.CASCADE)   # 每个lesson章节会有对应的视频
    name = models.CharField(max_length=100, verbose_name="lesson_video")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_name")
    url = models.CharField(max_length=200, verbose_name="video address", default='')
    learn_time = models.IntegerField(default=0, verbose_name="learn_time")

    class Meta:
        verbose_name="video"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="course",on_delete=models.CASCADE)    # course这个科目的文件资源
    name = models.CharField(max_length=100, verbose_name="resource file")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="add_name")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="resourse file",max_length=100)

    class Meta:
        verbose_name="resource"
        verbose_name_plural=verbose_name
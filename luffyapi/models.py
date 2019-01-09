from django.db import models


# Create your models here.


class Course(models.Model):
    """
    课程表
    """
    title = models.CharField(verbose_name='课程名', max_length=64)
    image = models.CharField(verbose_name='课程图片', max_length=32)
    level_choices = (
        (1, '初级'),
        (2, '中级'),
        (3, '高级'),
    )
    level = models.SmallIntegerField(verbose_name='难度', choices=level_choices, default=1)

    def __str__(self):
        return self.title


class CourseDetail(models.Model):
    """
    课程详情表
    """
    why = models.CharField(verbose_name='为什么报课程', max_length=32)
    course = models.OneToOneField(to='Course', verbose_name='课程', on_delete=models.CASCADE)
    recommend_courses = models.ManyToManyField(to='Course', verbose_name='相关推荐课程', related_name='re_course')

    def __str__(self):
        return self.course.title


class Chapters(models.Model):
    """
    章节表
    """
    title = models.CharField(verbose_name='章节名', max_length=32)
    course = models.ForeignKey(verbose_name='课程', to='Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Test(models.Model):
    name = models.CharField(verbose_name='名字', max_length=22)


class Test2(models.Model):
    test = models.ManyToManyField(to='Test')
    title = models.CharField(max_length=11)


# 用户表
class UserInfo(models.Model):
    user = models.CharField(verbose_name='用户名', max_length=64)
    pwd = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.user


# token表
class UserToken(models.Model):
    user = models.OneToOneField(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(verbose_name='token', max_length=128)
    expired = models.DateTimeField(verbose_name='有效期', auto_now_add=True)

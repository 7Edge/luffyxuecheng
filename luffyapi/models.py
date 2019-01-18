from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

# 课程大分类表，前端/后端
class CourseCategory(models.Model):
    """
    课程大分类表
    """
    name = models.CharField(verbose_name='课程类型', max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "01. 课程大表"

    def __str__(self):
        return "%s" % self.name


# 课程之分类表
class CourseSubCategory(models.Model):
    """
    课程子分类表
    """
    category = models.ForeignKey(verbose_name="所属大分类", to="CourseCategory", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="子课程类型", max_length=64)

    class Meta:
        verbose_name_plural = "02. 课程子表"

    def __str__(self):
        return "%s" % self.name


# 学位课程
class DegreeCourse(models.Model):
    """
    学位课程表
    """
    name = models.CharField(verbose_name='学位课程名', max_length=128, unique=True)
    course_img = models.CharField(verbose_name='课程示图', max_length=255)
    brief = models.TextField(verbose_name='学位课程简介')
    total_scholarship = models.PositiveIntegerField(verbose_name='总奖学金(里贝)', default=40000)
    mentor_compensation_bonus = models.PositiveIntegerField(verbose_name='本课程的导师辅导费用(里贝)', default=15000)
    period = models.PositiveIntegerField(verbose_name='建议学习周期（days)', default=150)  # 用于计算学位奖学金
    prerequisite = models.TextField(verbose_name='课程先修要求', max_length=1024)
    teachers = models.ManyToManyField(verbose_name='课程老师', to="Teacher")

    # 反向查询价格策略集，按周期计价,
    degree_price_policy_qs = GenericRelation(to='PricePolicy')

    # 反向查询课程问题集
    degree_asked_question = GenericRelation(to='OftenAskedQuestion')

    class Meta:
        verbose_name_plural = "03. 学位课程表"

    def __str__(self):
        return self.name


# 讲师 导师表
class Teacher(models.Model):
    """
    讲师 导师表
    """
    name = models.CharField(verbose_name='老师名', max_length=64)
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
    )
    role = models.SmallIntegerField(verbose_name='老师角色', choices=role_choices, default=0)
    title = models.CharField(verbose_name='职位/职称', max_length=64)
    signature = models.CharField(verbose_name='签名', max_length=255, blank=True, null=True)
    image = models.CharField(verbose_name='老师照片', max_length=255)
    brief = models.CharField(verbose_name='老师简介', max_length=1024)

    class Meta:
        verbose_name_plural = "04. 老师表"

    def __str__(self):
        return self.name


# 学位奖学金表
class Scholarship(models.Model):
    """
    学位课程奖学金表
    """
    degree_course = models.ForeignKey(verbose_name='学位课程', to="DegreeCourse", on_delete=models.CASCADE)
    time_percent = models.PositiveIntegerField(verbose_name='完成学位时间占比', help_text="只填写百分整数值，如90，代表90%")
    value = models.PositiveIntegerField(verbose_name='奖学金数额')

    class Meta:
        verbose_name_plural = '05. 学位奖学金表'

    def __str__(self):
        return "%s %s" % (self.degree_course, self.value)


# 专题课程表
class Course(models.Model):
    """
    专题课程 或 学位课程中的子模块课程 表
    """
    # title = models.CharField(verbose_name='课程名', max_length=64)  # 上一版本
    title = models.CharField(verbose_name='课程名', max_length=128, unique=True)
    # image = models.CharField(verbose_name='课程图片', max_length=32) # 上一版本
    image = models.CharField(verbose_name='课程图片', max_length=255)
    sub_category = models.ForeignKey(verbose_name='子课程分类', to='CourseSubCategory', on_delete=models.CASCADE)

    course_type_choices = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程模块'),
    )
    course_type = models.SmallIntegerField(verbose_name='专题课类型', choices=course_type_choices)
    degree_course = models.ForeignKey(verbose_name='学位课程', to="DegreeCourse",
                                      help_text='专题课程所属的学位课程,这里这填写关联的学位课程，可为空，表示不是学位课程',
                                      on_delete=models.SET_NULL, blank=True, null=True)

    brief = models.TextField(verbose_name='课程简介', max_length=2048)

    level_choices = (
        (1, '初级'),
        (2, '中级'),
        (3, '高级'),
    )
    level = models.SmallIntegerField(verbose_name='难度', choices=level_choices, default=2)

    pub_date = models.DateTimeField(verbose_name='课程发布日期', blank=True, null=True)
    period = models.PositiveIntegerField(verbose_name='建议学习周期(days)', default=7)
    order = models.IntegerField(verbose_name="课程顺序", help_text="从上一个课程数字往后排")
    attachment_path = models.CharField(verbose_name="课程课件路径", max_length=128, blank=True, null=True)
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    status = models.SmallIntegerField(verbose_name="课程状态", default=0)
    template_id = models.SmallIntegerField(verbose_name="前端模板ID", default=1)

    # 反向查询课程价格按周期价格策略集
    course_price_policy_qs = GenericRelation(to="PricePolicy")

    # 反向查询课程常见问题集
    course_asked_question_qs = GenericRelation(to="OftenAskedQuestion")

    class Meta:
        verbose_name_plural = "06. 专题课程表"

    def __str__(self):
        return self.title


# 专题课程详情内容，一对一
class CourseDetail(models.Model):
    """
    课程详情表
    """
    course = models.OneToOneField(to='Course', verbose_name='课程', on_delete=models.CASCADE)
    hours = models.IntegerField(verbose_name='课时')
    course_slogan = models.CharField(verbose_name='口号', max_length=125, blank=True, null=True)
    video_brief_link = models.CharField(verbose_name='课程简介视频', max_length=255, blank=True, null=True)
    why = models.CharField(verbose_name='为什么报课程', max_length=255)
    what_to_study_brief = models.TextField(verbose_name='将会学到什么')
    career_improvement = models.TextField(verbose_name='此项目如何有助于我的职业生涯')
    prerequisite = models.TextField(verbose_name='课程先修条件', max_length=1024)

    recommend_courses = models.ManyToManyField(to='Course', verbose_name='相关推荐课程', related_name='re_course',
                                               blank=True)
    teachers = models.ManyToManyField(verbose_name='任课老师', to='Teacher')

    class Meta:
        verbose_name_plural = "07. 专题课程详情表"

    def __str__(self):
        return self.course


# 课程咨询常见问题
class OftenAskedQuestion(models.Model):
    """
    常见问题表，有一个联合主键
    """
    question = models.CharField(verbose_name='常见问题', max_length=255)
    answer = models.CharField(verbose_name='答案', max_length=255)

    object_id = models.IntegerField(verbose_name='关联对象ID', help_text="多个表的对象主键")
    content_type = models.ForeignKey(verbose_name='所属表的类型', to=ContentType, on_delete=models.CASCADE,
                                     help_text='外键引用ContentType的主键')
    generic_fk_to_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        verbose_name_plural = "08. 常见问题表"
        unique_together = ('question', 'object_id', 'content_type')

    def __str__(self):
        return "%s-%s" % (self.generic_fk_to_object, self.question)


# 课程大纲
class CourseOutline(models.Model):
    """
    课程大纲表
    """
    course_detail = models.ForeignKey(verbose_name='课程详情', to='CourseDetail', on_delete=models.CASCADE)

    order = models.PositiveIntegerField(verbose_name='显示顺序', default=1)  # 前端显示的顺序

    title = models.CharField(verbose_name='标题', max_length=255)
    content = models.CharField(verbose_name='大纲内容', max_length=2048)

    class Meta:
        verbose_name_plural = '09. 大纲表'
        unique_together = ('course_detail', 'title')

    def __str__(self):
        return self.title


# 课程章节
class Chapters(models.Model):
    """
    章节表，课程的大模块
    """
    title = models.CharField(verbose_name='章节名', max_length=32)
    chapter = models.IntegerField(verbose_name='章节号')
    summary = models.TextField(verbose_name='章节介绍', blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name='发布日期', auto_now_add=True)

    course = models.ForeignKey(verbose_name='课程', to='Course', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "10. 课程章节"
        unique_together = ('course', 'chapter')

    def __str__(self):
        return "%s(第%s章) %s" % (self.course, self.chapter, self.title)


# 章节每节课
class CourseSection(models.Model):
    """
    每节课
    """
    name = models.CharField(verbose_name='课名', max_length=128)
    order = models.IntegerField(verbose_name='课序', help_text='建议每个课时之间空1至2个值，以备后续插入课时')
    section_type_choices = (
        (0, '文档'),
        (1, '视频'),
        (2, '练习'),
    )
    section_type = models.SmallIntegerField(verbose_name='课类型', choices=section_type_choices, default=1)
    section_link = models.CharField(verbose_name='连接文件', max_length=255, help_text='如果是视频类型，填写vid,如果是文档，填link')

    video_time = models.CharField(verbose_name='视频时长', max_length=32, blank=True, null=True)

    pub_date = models.DateTimeField(verbose_name='发布日期', auto_now_add=True)
    free_trail = models.BooleanField(verbose_name='是否可试看', default=False)

    chapter = models.ForeignKey(verbose_name='章节', to='Chapters', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '11. 课节表'
        unique_together = ('chapter', 'section_link')

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


# 作业
class HomeWork(models.Model):
    """
    作业表
    """
    title = models.CharField(verbose_name='作业题目', max_length=128)
    order = models.SmallIntegerField(verbose_name='作业顺序', help_text="同一课程的每个作业之前的order值间隔1-2个数")
    homework_type_choices = (
        (0, '作业'),
        (1, '模块通关考核')
    )
    homework_type = models.SmallIntegerField(verbose_name='作业类型', choices=homework_type_choices, default=0)
    requirement = models.CharField(verbose_name='作业需求', max_length=1024)
    threshold = models.TextField(verbose_name='踩分点', max_length=1024)
    recommend_period = models.PositiveSmallIntegerField(verbose_name='推荐完成周期(天)', default=7)
    scholarship = models.PositiveSmallIntegerField(verbose_name='为该作业分配的奖学金(贝里)')
    note = models.TextField(verbose_name='注意提示', blank=True, null=True)
    enabled = models.BooleanField(default=True, help_text="本作业如果后期不需要了，不想让学员看到，可以设置为False")

    chapter = models.ForeignKey(verbose_name='章节', to='Chapters', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "12. 章节作业"
        unique_together = ('chapter', 'title')

    def __str__(self):
        return "%s - %s" % (self.chapter, self.title)


# 价格策略 重要的表
class PricePolicy(models.Model):
    """
    价格策略表， 将学位课和专题课的价格策略都放在这里。主要策略的不同维度是周期不同
    """
    valid_period_choices = (
        (1, '1天'), (3, '3天'),
        (7, '1周'), (14, '2周'),
        (30, '1个月'),
        (60, '2个月'),
        (90, '3个月'),
        (180, '6个月'), (210, '12个月'),
        (540, '18个月'), (720, '24个月'),
    )
    period = models.PositiveSmallIntegerField(verbose_name='学习周期', choices=valid_period_choices)
    price = models.FloatField()

    object_id = models.IntegerField(verbose_name='课程对象')
    content_type = models.ForeignKey(verbose_name='对应类型', to=ContentType, on_delete=models.CASCADE)

    generic_fk_to_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        verbose_name_plural = "13. 价格策略表"
        unique_together = ('object_id', 'content_type', 'price')


# class Test(models.Model):
#     name = models.CharField(verbose_name='名字', max_length=22)
#
#
# class Test2(models.Model):
#     test = models.ManyToManyField(to='Test')
#     title = models.CharField(max_length=11)


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

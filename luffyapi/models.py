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
        return "%s" % self.course


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

    class Meta:
        verbose_name_plural = '201. 学城用户表'

    def __str__(self):
        return self.user


# token表
class UserToken(models.Model):
    user = models.OneToOneField(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(verbose_name='token', max_length=128)
    expired = models.DateTimeField(verbose_name='有效期', auto_now_add=True)

    class Meta:
        verbose_name_plural = '202. 用户认证token表'

    def __str__(self):
        return "%s - %s" % (self.user, self.token)


# 账号表
class Account(models.Model):
    """
    账号
    """
    user = models.OneToOneField(verbose_name='用户', to="UserInfo", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '203. 账户表'

    def __str__(self):
        return self.user


# 深科技 文章来源
class ArticleSource(models.Model):
    """
    文章来源
    """
    name = models.CharField(verbose_name='文章来源', max_length=128, unique=True)

    class Meta:
        verbose_name_plural = '3001. 深科技文章来源'

    def __str__(self):
        return self.name


# 文章资讯
class Article(models.Model):
    """
    文章详情
    未完：点赞反向查询了GenericRelation字段
    """
    title = models.CharField(verbose_name='标题', max_length=255, unique=True, db_index=True)
    source = models.ForeignKey(verbose_name='来源', to='ArticleSource', on_delete=models.CASCADE)
    article_type_choices = (
        (0, '资讯'),
        (1, '视频')
    )
    article_type = models.SmallIntegerField(verbose_name='文章类型', choices=article_type_choices, default=0)
    brief = models.TextField(verbose_name='文章概要', max_length=512)
    head_img = models.CharField(verbose_name='文章头贴图', max_length=255)
    content = models.TextField(verbose_name='正文内容')
    pub_date = models.DateTimeField(verbose_name='上架日期')
    offline_date = models.DateTimeField(verbose_name='下架日期')
    status_choices = (
        (0, '在线'),
        (1, '下线')
    )
    status = models.SmallIntegerField(verbose_name='文章状态', choices=status_choices, default=0)
    order = models.SmallIntegerField(verbose_name='权重', default=0, help_text='文章想置顶，可以把数字调大，'
                                                                             '不要超过1000')
    vid = models.CharField(verbose_name='视频VID', max_length=128, help_text='文章类型是视频，则需要添加视频VID',
                           blank=True, null=True)
    comment_num = models.SmallIntegerField(verbose_name='评论数', default=0)
    agree_num = models.SmallIntegerField(verbose_name='点赞数', default=0)
    view_num = models.SmallIntegerField(verbose_name='浏览数', default=0)
    collect_num = models.SmallIntegerField(verbose_name='收藏数', default=0)

    tags = models.ManyToManyField(verbose_name='标签', to="Tags", blank=True)

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)

    position_choices = (
        (0, '信息流'),
        (1, 'banner大图'),
        (2, 'banner小图')
    )
    position = models.SmallIntegerField(verbose_name='位置', choices=position_choices, default=0)

    # 评论反向查询字段
    comment_num_qs = GenericRelation(to='Comment')

    # 收藏反向查询字段
    collect_num_qs = GenericRelation(to='Collection')

    # 点赞反向查询字段

    class Meta:
        verbose_name_plural = '3002. 深科技文章表'

    def __str__(self):
        return self.title


# 通用收藏表
class Collection(models.Model):
    """
    通用收藏表
    """
    content_type = models.ForeignKey(verbose_name='类型', to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='对象')
    generic_fk_to_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    account = models.ForeignKey("Account", verbose_name='账号', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='收藏日期', auto_now_add=True)

    class Meta:
        verbose_name_plural = '40001. 通用收藏表'
        unique_together = ('content_type', 'object_id', 'account')


# 通用评论表
class Comment(models.Model):
    """
    通用评论表
    """
    content_type = models.ForeignKey(verbose_name='类型', to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='对象')
    generic_fk_to_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    p_node = models.ForeignKey(verbose_name='父评论', to='self', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(verbose_name='内容', max_length=1024)
    account = models.ForeignKey(verbose_name='账号', to='Account', on_delete=models.CASCADE)
    disagree_number = models.IntegerField(verbose_name='踩', default=0)
    agree_number = models.IntegerField(verbose_name='赞', default=0)
    date = models.DateTimeField(verbose_name='评论日期', auto_now_add=True)

    class Meta:
        verbose_name_plural = '40002. 通用评论表'

    def __str__(self):
        return self.content


# 通用标签表
class Tags(models.Model):
    """
    这里的标签，不是通过contenttype,是利用一个分类，这种在关联查询时，就必须自己知道类型,不是用表名来分类。
    """
    tag_type_choices = (
        (0, '文章标签'),
        (1, '课程评价标签'),
        (2, '用户感兴趣技术标签')
    )
    tag_type = models.SmallIntegerField(verbose_name='标签类型', choices=tag_type_choices)
    name = models.CharField(verbose_name='标签名', max_length=64)

    class Meta:
        unique_together = ('name', 'tag_type')
        verbose_name_plural = '40003. 标签集合表'

    def __str__(self):
        return "%s:%s" % (self.get_tag_type_display, self.name)

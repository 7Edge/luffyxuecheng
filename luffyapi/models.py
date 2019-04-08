import hashlib

from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

"""
总共45张表
"""


# 1 课程大分类表，前端/后端
class CourseCategory(models.Model):
    """
    课程大分类表
    """
    name = models.CharField(verbose_name='课程类型', max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "01. 课程大表"

    def __str__(self):
        return "%s" % self.name


# 2 课程之分类表
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


# 3 学位课程
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


# 4 讲师 导师表
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


# 5 学位奖学金表
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


# 6 专题课程表
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
    status = models.SmallIntegerField(verbose_name="课程状态", choices=status_choices, default=0)
    template_id = models.SmallIntegerField(verbose_name="前端模板ID", default=1)

    # 反向查询课程价格按周期价格策略集
    course_price_policy_qs = GenericRelation(to="PricePolicy")

    # 反向查询课程常见问题集
    course_asked_question_qs = GenericRelation(to="OftenAskedQuestion")

    class Meta:
        verbose_name_plural = "06. 专题课程表"

    def __str__(self):
        return self.title


# 7 专题课程详情内容，一对一
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


# 8 课程咨询常见问题
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


# 9 课程大纲
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


# 10 课程章节
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


# 11 章节每节课
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


# 12 作业
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


# 13 报名学生作业记录
class HomeworkRecord(models.Model):
    """学员作业记录及成绩"""
    homework = models.ForeignKey(to="HomeWork", on_delete=models.CASCADE)
    student = models.ForeignKey("EnrolledDegreeCourse", verbose_name="学生", on_delete=models.CASCADE)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (-1, 'D'),
                     (0, 'N/A'),
                     (-100, 'COPY'),
                     )
    score = models.SmallIntegerField(verbose_name="分数", choices=score_choices, null=True, blank=True)
    mentor = models.ForeignKey("Account", related_name="my_stu_homework_record", limit_choices_to={'role': 1},
                               verbose_name="导师", on_delete=models.CASCADE)
    mentor_comment = models.TextField(verbose_name="导师批注", blank=True, null=True)  # 导师
    status_choice = (
        (0, '待批改'),
        (1, '已通过'),
        (2, '不合格'),
    )
    status = models.SmallIntegerField(verbose_name='作业状态', choices=status_choice, default=0)

    submit_num = models.SmallIntegerField(verbose_name='提交次数', default=0)
    correct_date = models.DateTimeField('备注日期', blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField("作业提交日期", auto_now_add=True)

    check_date = models.DateTimeField("批改日期", null=True, blank=True)

    update_time = models.DateTimeField(auto_now=True, verbose_name="提交日期")

    # homework_path = models.CharField(verbose_name='作业路径', max_length=256,blank=True,null=True) 作业路径可以动态拿到，没必要存

    reward_choice = ((0, '新提交'),
                     (1, '按时提交'),
                     (2, '未按时提交'),
                     (3, '成绩已奖励'),
                     (4, '成绩已处罚'),
                     (5, '未作按时检测'),
                     )
    reward_status = models.SmallIntegerField(verbose_name='作业记录奖惩状态', default=0)

    def __str__(self):
        return "%s %s" % (self.homework, self.student)

    class Meta:
        verbose_name_plural = "13. 作业"
        unique_together = ("homework", "student")


# 14 导师组
class MentorGroup(models.Model):
    """
    导师组
    """
    name = models.CharField(verbose_name='导师组名', max_length=64, unique=True)
    brief = models.TextField(verbose_name='简介brief', blank=True, null=True)
    mentors = models.ManyToManyField(verbose_name='组员', to='Account', limit_choices_to={'role': 1})

    class Meta:
        verbose_name_plural = '14. 导师组'

    def __str__(self):
        return self.name


# 15 学位课程，每个模块的学习计划。计划时间，计划作业。
class CourseSchedule(models.Model):
    """课程进度计划表,针对学位课程，每开通一个模块，就为这个学员生成这个模块的推荐学习计划表，后面的奖惩均按此表进行"""
    study_record = models.ForeignKey(to="StudyRecord", on_delete=models.CASCADE)
    homework = models.ForeignKey(to="HomeWork", on_delete=models.CASCADE)
    recommend_date = models.DateField("推荐交作业日期")

    def __str__(self):
        return "%s - %s - %s " % (self.study_record, self.homework, self.recommend_date)

    class Meta:
        unique_together = ('study_record', 'homework')
        verbose_name_plural = "15. 课程模块计划表（学位课）"


# 16 学位课程，每个学生报名的学位课程的每个模块有一个学习记录。
class StudyRecord(models.Model):
    """学位课程的模块学习进度，报名学位课程后，每个模块会立刻生成一条学习纪录"""
    enrolled_degree_course = models.ForeignKey(to="EnrolledDegreeCourse", on_delete=models.CASCADE)
    course_module = models.ForeignKey(to="Course", verbose_name="学位模块", limit_choices_to={'course_type': 2},
                                      on_delete=models.CASCADE)
    open_date = models.DateField(blank=True, null=True, verbose_name="开通日期")
    end_date = models.DateField(blank=True, null=True, verbose_name="完成日期")
    status_choices = ((2, '在学'), (1, '未开通'), (0, '已完成'))
    status = models.SmallIntegerField(choices=status_choices, default=1)

    class Meta:
        verbose_name_plural = "16. 学习记录表（报名学位课程后，每个模块会立刻生成一条学习纪录）"
        unique_together = ('enrolled_degree_course', 'course_module')

    def __str__(self):
        return '%s-%s' % (self.enrolled_degree_course, self.course_module)

    def save(self, *args, **kwargs):
        if self.course_module.degree_course_id != self.enrolled_degree_course.degree_course_id:
            raise ValueError("学员要开通的模块必须与其报名的学位课程一致！")

        super(StudyRecord, self).save(*args, **kwargs)


# 17 报名学位课程，购买后学位课程后，要学习学位课程前，都需要进行报名，通过报名登记，触发相关报名后的操作。(报名的老师，触发第一模块开通，
# 相关学习记录的生成)
class EnrolledDegreeCourse(models.Model):
    """已报名的学位课程"""
    account = models.ForeignKey(to="Account", on_delete=models.CASCADE)
    degree_course = models.ForeignKey(to="DegreeCourse", on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    # 开通第一个模块时，再添加课程有效期，2年
    valid_begin_date = models.DateField(verbose_name="有效期开始自", blank=True, null=True)
    valid_end_date = models.DateField(verbose_name="有效期结束至", blank=True, null=True)
    status_choices = (
        (0, '在学中'),
        (1, '休学中'),
        (2, '已毕业'),
        (3, '超时结业'),
        (4, '未开始'),
        # (3, '其它'),
    )
    study_status = models.SmallIntegerField(choices=status_choices, default=0)
    mentor = models.ForeignKey(to="Account", verbose_name="导师", related_name='my_students',
                               blank=True, null=True, limit_choices_to={'role': 1}, on_delete='')
    mentor_fee_balance = models.PositiveIntegerField("导师费用余额", help_text="这个学员的导师费用，每有惩罚，需在此字段同时扣除")
    order_detail = models.OneToOneField(to="OrderDetail", on_delete=models.CASCADE)  # 使订单购买后支持填写报名表

    def __str__(self):
        return "%s:%s" % (self.account, self.degree_course)

    class Meta:
        unique_together = ('account', 'degree_course')
        verbose_name_plural = "17. 报名学位课"


# 18 报名表格详情信息
class DegreeRegistrationForm(models.Model):
    """学位课程报名表"""
    enrolled_degree = models.OneToOneField("EnrolledDegreeCourse", on_delete=models.CASCADE)
    current_company = models.CharField(max_length=64, )
    current_position = models.CharField(max_length=64, )
    current_salary = models.IntegerField()
    work_experience_choices = ((0, "应届生"),
                               (1, "1年"),
                               (2, "2年"),
                               (3, "3年"),
                               (4, "4年"),
                               (5, "5年"),
                               (6, "6年"),
                               (7, "7年"),
                               (8, "8年"),
                               (9, "9年"),
                               (10, "10年"),
                               (11, "超过10年"),
                               )
    work_experience = models.IntegerField()
    open_module = models.BooleanField("是否开通第1模块", default=True)
    stu_specified_mentor = models.CharField("学员自行指定的导师名", max_length=32, blank=True, null=True)
    study_plan_choices = ((0, "1-2小时/天"),
                          (1, "2-3小时/天"),
                          (2, "3-5小时/天"),
                          (3, "5小时+/天"),
                          )
    study_plan = models.SmallIntegerField(choices=study_plan_choices, default=1)
    why_take_this_course = models.TextField("报此课程原因", max_length=1024)
    why_choose_us = models.TextField("为何选路飞", max_length=1024)
    your_expectation = models.TextField("你的期待", max_length=1024)
    memo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "18. 报名表（学位课）"

    def __str__(self):
        return "%s" % self.enrolled_degree


# 19 专题课程报名
class EnrolledCourse(models.Model):
    """已报名课程,不包括学位课程"""
    account = models.ForeignKey(to="Account", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", limit_choices_to=~Q(course_type=2), on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    valid_begin_date = models.DateField(verbose_name="有效期开始自")
    valid_end_date = models.DateField(verbose_name="有效期结束至")
    status_choices = ((0, '已开通'), (1, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    order_detail = models.OneToOneField("OrderDetail", on_delete=models.CASCADE)  # 使订单购买后支持 课程评价

    # order = models.ForeignKey("Order",blank=True,null=True)

    def __str__(self):
        return "%s:%s" % (self.account, self.course)

    class Meta:
        verbose_name_plural = "19. 报名专题课"


# 20 价格策略 重要的表
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
        verbose_name_plural = "20. 价格策略表"
        unique_together = ('object_id', 'content_type', 'price')

    def __str__(self):
        return "%s - 周期（%s）" % (self.generic_fk_to_object, self.get_period_display())


# 21 用户表
class UserInfo(models.Model):
    user = models.CharField(verbose_name='用户名', max_length=64)
    pwd = models.CharField(verbose_name='密码', max_length=64)

    class Meta:
        verbose_name_plural = '201. 学城用户表'

    def __str__(self):
        return self.user


# 22 token表
class UserToken(models.Model):
    user = models.OneToOneField(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(verbose_name='token', max_length=128)
    expired = models.DateTimeField(verbose_name='有效期', auto_now_add=True)

    class Meta:
        verbose_name_plural = '202. 用户认证token表'

    def __str__(self):
        return "%s - %s" % (self.user, self.token)

    # 暂时由代码层面实现
    # def save(self, *args, **kwargs):
    #     import datetime
    #     # 根据用户名和时间生成唯一标识
    #
    #     self.token = self.generate_key()
    #     self.created = datetime.datetime.utcnow()
    #     return super(UserToken, self).save(*args, **kwargs)
    #
    # def generate_key(self):
    #     import datetime
    #
    #     """根据用户名和时间生成唯一标识"""
    #     username = self.user.user
    #     now = str(datetime.datetime.now()).encode('utf-8')
    #     md5 = hashlib.md5(username.encode('utf-8'))
    #     md5.update(now)
    #     return md5.hexdigest()


# 23 账号表
class Account(models.Model):
    """
    账号
    """
    user = models.OneToOneField(verbose_name='用户', to="UserInfo", on_delete=models.CASCADE)
    # 与第三方交互用户信息时，用这个uid,已避免泄露敏感用户信息给第三方。如，微信绑定时或者提供用户给CC视频。
    uid = models.CharField(verbose_name='唯一ID', max_length=255, help_text='用户名的md5值,不用填写', unique=True, blank=True)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    mobile = models.BigIntegerField(verbose_name="手机", unique=True, help_text="用于手机验证码登录")
    qq = models.CharField(verbose_name="QQ", max_length=64, blank=True, null=True, db_index=True)
    weixin = models.CharField(max_length=128, blank=True, null=True, db_index=True, verbose_name="微信")
    wx_openid = models.CharField(max_length=128, blank=True, null=True, db_index=True, verbose_name="微信openid")

    # 个人资料
    # 职位相关信息，注册时必选
    profession = models.ForeignKey("Profession", verbose_name="职位信息", blank=True, null=True, on_delete=models.CASCADE)
    # 所在城市，注册时必填, 通过城市能找到对应的省份
    city = models.ForeignKey("City", verbose_name="城市", blank=True, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tags", blank=True, verbose_name="感兴趣的标签")
    signature = models.CharField('个人签名', blank=True, null=True, max_length=255)
    brief = models.TextField("个人介绍", blank=True, null=True)

    gender_choices = ((0, '保密'), (1, '男'), (2, '女'))
    gender = models.SmallIntegerField(choices=gender_choices, default=0, verbose_name="性别")
    degree_choices = ((0, "学历"), (1, '高中以下'), (2, '中专／高中'), (3, '大专'), (4, '本科'), (5, '硕士'), (6, '博士'))
    degree = models.PositiveSmallIntegerField(choices=degree_choices, blank=True,
                                              null=True, default=0, verbose_name="学历")
    birthday = models.DateField(blank=True, null=True, verbose_name="生日")
    id_card = models.CharField(max_length=32, blank=True, null=True, verbose_name="身份证号或护照号")
    # password = models.CharField('password', max_length=128,
    #                             help_text=mark_safe('''<a class='btn-link' href='password'>重置密码</a>'''))

    is_active = models.BooleanField(default=True, verbose_name="账户状态")
    is_staff = models.BooleanField(verbose_name='staff status', default=False, help_text='决定着用户是否可登录管理后台')
    name = models.CharField(max_length=32, default="", verbose_name="真实姓名")
    head_img = models.CharField(max_length=128, default='/static/frontend/head_portrait/logo@2x.png',
                                verbose_name="个人头像")

    role_choices = ((0, '学生'),
                    (1, '导师'),
                    (2, '讲师'),
                    (3, '管理员'))
    role = models.SmallIntegerField(verbose_name='角色', choices=role_choices, default=0)

    # 贝里余额
    balance = models.PositiveIntegerField(default=0, verbose_name="可提现和使用余额")

    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta:
        verbose_name_plural = '203. 账户表'

    def __str__(self):
        return str(self.user)

    # 创建用户是，自动生成uid在保存用户时
    def save(self, *args, **kwargs):
        if not self.pk:
            md5_obj = hashlib.md5()
            md5_obj.update(self.user.user.encode(encoding='utf8'))
            self.uid = md5_obj.hexdigest()
        super().save(*args, **kwargs)


# 24 省份表
class Province(models.Model):
    code = models.IntegerField(verbose_name='省代码', unique=True)
    name = models.CharField(verbose_name='省名称', max_length=64, unique=True)

    class Meta:
        verbose_name_plural = '204. 省份表'

    def __str__(self):
        return "%s - %s" % (self.code, self.name)


# 25 城市表
class City(models.Model):
    code = models.IntegerField(verbose_name='城市码', unique=True)
    name = models.CharField(verbose_name='城市名', max_length=64)
    province = models.ForeignKey(verbose_name='省份', to='Province', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '205. 城市表'

    def __str__(self):
        return '%s - %s' % (self.code, self.name)


# 26 行业表
class Industry(models.Model):
    code = models.IntegerField(verbose_name='行业代码', unique=True)
    name = models.CharField(verbose_name='行业名称', max_length=128, unique=True)

    class Meta:
        verbose_name_plural = '206. 行业表'

    def __str__(self):
        return "%s - %s" % (self.code, self.name)


# 27 职业表
class Profession(models.Model):
    """
    职位关联所属行业
    """
    code = models.IntegerField(verbose_name='职业代码')
    name = models.CharField(verbose_name='职业名称', max_length=64)
    industry = models.ForeignKey(verbose_name='所属行业', to='Industry', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "207. 职业表"

    def __str__(self):
        return "%s - %s" % (self.code, self.name)


# 28 用户反馈表
class Feedback(models.Model):
    name = models.CharField(verbose_name='标题', max_length=32, blank=True, null=True)
    contact = models.CharField(verbose_name='联系方式', max_length=64, blank=True, null=True)
    feedback_type_choices = ((0, '网站优化建议'), (1, '烂!我想吐槽'), (2, '网站bug反馈'))
    feedback_type = models.SmallIntegerField(verbose_name='反馈类型', choices=feedback_type_choices, default=0)
    content = models.TextField(verbose_name='反馈内容', max_length=1024)
    date = models.DateTimeField(verbose_name='反馈时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '208. 反馈表'

    def __str__(self):
        return self.name


# 29 深科技 文章来源
class ArticleSource(models.Model):
    """
    文章来源
    """
    name = models.CharField(verbose_name='文章来源', max_length=128, unique=True)

    class Meta:
        verbose_name_plural = '3001. 深科技文章来源'

    def __str__(self):
        return self.name


# 30 文章资讯
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


# 31 通用收藏表
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


# 32 通用评论表
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


# 33 通用标签表
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


# 34 奖惩规则
class ScoreRule(models.Model):
    """积分规则，学位课才有奖惩，涉及学位老师，学位学生"""
    score_rule_choices = (
        (0, '未按时交作业'),
        (1, '未及时批改作业'),
        (2, '作业成绩'),
        (3, '未在规定时间内对学员进行跟进'),
        (4, '未在规定时间内回复学员问题'),
        (5, '收到学员投诉'),
        (6, '导师相关'),
        (7, '学位奖学金'),
    )
    rule = models.SmallIntegerField(choices=score_rule_choices, verbose_name="积分规则")
    score_type_choices = ((0, '奖励'), (1, '惩罚'), (2, '初始分配'))
    score_type = models.SmallIntegerField(choices=score_type_choices, verbose_name="奖惩", default=0)
    score = models.IntegerField(help_text="扣分数与贝里相等,若为0则代表规则的值可以从别处取得")
    # maturity_days = models.IntegerField("成熟周期", help_text="自纪录创建时开始计算")
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s-%s:%s" % (self.get_rule_display(), self.get_score_type_display(), self.score)

    class Meta:
        unique_together = ('rule', 'score_type')
        verbose_name_plural = "6000001. 奖惩规则"


# 35 奖惩记录
class ScoreRecord(models.Model):
    """积分奖惩记录，学位课才有奖惩"""
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, verbose_name="关联学位课程",
                                      on_delete=models.CASCADE)
    score_rule = models.ForeignKey("ScoreRule", verbose_name="关联规则", on_delete=models.CASCADE)
    account = models.ForeignKey("Account", verbose_name="被执行人", on_delete=models.CASCADE)
    score = models.IntegerField(
        verbose_name="金额(贝里)")  # 这里单独有一个字段存积分而不是从score_rule里引用的原因是考虑到如果引用的话， # 一旦score_rule里的积分有变更，那么所有用户的历史积分也会被影响
    received_score = models.IntegerField("实际到账金额贝里)", help_text="仅奖励用", default=0)
    balance = models.PositiveIntegerField(verbose_name="奖金余额(贝里)")

    maturity_date = models.DateField("成熟日期(可提现日期)")
    applied = models.BooleanField(default=False, help_text="奖赏纪录是否已被执行", verbose_name="是否已被执行")
    applied_date = models.DateTimeField(blank=True, null=True, verbose_name="事件生效日期")
    date = models.DateTimeField(auto_now_add=True, verbose_name="事件触发日期")
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s-%s - %s - %s 奖金余额:%s" % (self.id, self.score_rule, self.account, self.score, self.balance)

    class Meta:
        verbose_name_plural = "6000002. 奖惩记录"


# 36 课程优惠卷
class Coupon(models.Model):
    """优惠卷类型"""

    name = models.CharField(verbose_name='优惠券名', max_length=64)
    brief = models.TextField(verbose_name='优惠券介绍', null=True, blank=True)
    coupon_type_choices = ((0, '通用券'),
                           (1, '折扣券'),
                           (2, '满减券'))
    coupon_type = models.SmallIntegerField(verbose_name='券类型', choices=coupon_type_choices)

    money_equivalent_value = models.IntegerField(verbose_name='等值货币', null=True, blank=True)
    off_percent = models.PositiveIntegerField(verbose_name="折扣百分比", help_text="只针对折扣券，例7.9折，写79",
                                              null=True, blank=True)
    minimum_consume = models.PositiveIntegerField(verbose_name='最低消费', default=0, help_text="仅在满减券时填写此字段")

    object_id = models.PositiveIntegerField(verbose_name='课程id', blank=True, null=True, help_text='通用卷不用绑定课程')
    content_type = models.ForeignKey(verbose_name='课程类型', to=ContentType, null=True, blank=True,
                                     on_delete=models.CASCADE)
    content_object = GenericForeignKey()

    quantity = models.PositiveIntegerField(verbose_name='优惠券数量', default=1)
    open_date = models.DateField(verbose_name='优惠券领取开始时间')
    close_date = models.DateField(verbose_name='优惠券领取结束时间')
    valid_begin_date = models.DateField(verbose_name='有效期开始时间', null=True, blank=True)
    valid_end_date = models.DateField(verbose_name='有效期结束时间', null=True, blank=True)
    coupon_valid_days = models.PositiveIntegerField(verbose_name='优惠卷有效期(天)', blank=True, null=True,
                                                    help_text='自从券被领取时开始算起')

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)

    class Meta:
        verbose_name_plural = "500001. 优惠卷类型"

    def __str__(self):
        return "%s(%s)" % (self.get_coupon_type_display(), self.name)

    def save(self, *args, **kwargs):
        if not self.coupon_valid_days or (self.valid_begin_date and self.valid_end_date):
            if self.valid_begin_date and self.valid_end_date:
                if self.valid_end_date <= self.valid_begin_date:
                    raise ValueError("valid_end_date 有效期结束日期必须晚于 valid_begin_date ")
            if self.coupon_valid_days == 0:
                raise ValueError("coupon_valid_days 有效期不能为0")
        if self.close_date < self.open_date:
            raise ValueError("close_date 优惠券领取结束时间必须晚于 open_date优惠券领取开始时间 ")

        super(Coupon, self).save(*args, **kwargs)


# 37 优惠卷记录
class CouponRecord(models.Model):
    """优惠券发放，优惠券消费记录"""
    account = models.ForeignKey(verbose_name='所属账户', to='UserInfo', on_delete=models.CASCADE)
    coupon = models.ForeignKey(verbose_name="优惠券类型", to='Coupon', on_delete=models.CASCADE)
    coupon_number = models.CharField(verbose_name='优惠卷编号', max_length=64, unique=True)

    status_choices = ((0, '未使用'),
                      (1, '已使用'),
                      (2, '已过期'))
    status = models.SmallIntegerField(verbose_name='优惠卷状态', choices=status_choices, default=0)
    get_time = models.DateTimeField(verbose_name='领取时间', help_text='用户领取时间')
    used_time = models.DateTimeField(verbose_name='使用时间', null=True, blank=True)

    order = models.ForeignKey(verbose_name='使用的订单', to="Order", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "500002. 优惠卷记录"

    def __str__(self):
        return '%s-%s-%s' % (self.account, self.coupon_number, self.status)


# 38 订单表
class Order(models.Model):
    """订单"""
    payment_type_choices = ((0, '微信'), (1, '支付宝'), (2, '优惠码'), (3, '贝里'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices)

    payment_number = models.CharField(max_length=128, verbose_name="支付第3方订单号", null=True, blank=True)
    order_number = models.CharField(max_length=128, verbose_name="订单号", unique=True)  # 考虑到订单合并支付的问题
    account = models.ForeignKey(to="Account", verbose_name='账号', on_delete=models.CASCADE)
    actual_amount = models.FloatField(verbose_name="实付金额")

    status_choices = ((0, '交易成功'), (1, '待支付'), (2, '退费申请中'), (3, '已退费'), (4, '主动取消'), (5, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")

    class Meta:
        verbose_name_plural = "70000001. 订单表"

    def __str__(self):
        return "%s" % self.order_number


# 39 订单详情表
class OrderDetail(models.Model):
    """订单详情"""
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE)

    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)  # 可关联普通课程或学位
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    original_price = models.FloatField("课程原价")
    price = models.FloatField("折后价格")
    content = models.CharField(max_length=255, blank=True, null=True)  # ？
    valid_period_display = models.CharField("有效期显示", max_length=32)  # 在订单页显示
    valid_period = models.PositiveIntegerField("有效期(days)")  # 课程有效期
    memo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.order, self.content_type, self.price)

    class Meta:
        verbose_name_plural = "70000002. 订单详细"
        unique_together = ("order", 'content_type', 'object_id')


# 40 贝里交易记录
class TransactionRecord(models.Model):
    """贝里交易纪录"""
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    amount = models.IntegerField("金额")
    # balance = models.IntegerField("账户余额")
    transaction_type_choices = ((0, '收入'), (1, '支出'), (2, '退款'), (3, "提现"))  # 2 为了处理 订单过期未支付时，锁定期贝里的回退
    transaction_type = models.SmallIntegerField(choices=transaction_type_choices)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="关联对象")
    content_object = GenericForeignKey('content_type', 'object_id')

    transaction_number = models.CharField(unique=True, verbose_name="流水号", max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name_plural = "70000003. 贝里交易记录"

    def __str__(self):
        return "%s" % self.transaction_number


# 41
class StuFollowUpRecord(models.Model):
    """学员跟进记录"""
    enrolled_degree_course = models.ForeignKey("EnrolledDegreeCourse", verbose_name="学生", on_delete=models.CASCADE)
    mentor = models.ForeignKey("Account", related_name='mentor', limit_choices_to={'role': 1}, verbose_name="导师",
                               on_delete=models.CASCADE)
    followup_tool_choices = ((0, 'QQ'), (1, '微信'), (2, '电话'), (3, '系统通知'))
    followup_tool = models.SmallIntegerField(choices=followup_tool_choices, default=1)
    record = models.TextField(verbose_name="跟进记录")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="跟进记录的截图等")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "800000001. 学员跟进记录"

    def __str__(self):
        return "%s --%s --%s" % (self.enrolled_degree_course, self.record, self.date)


# 42
class Question(models.Model):
    """课程提问"""
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name="问题概要", db_index=True)
    question_type_choices = ((0, '专题课程问题'), (1, '学位课程问题'))
    question_type = models.SmallIntegerField(choices=question_type_choices, default=0, verbose_name="来源")
    account = models.ForeignKey("Account", verbose_name="提问者", on_delete=models.CASCADE)
    # 若是针对整个学位课程的提问，关联这个
    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, on_delete=models.CASCADE)
    # 针对整个学位课程的提问不需关联特定课时
    course_section = models.ForeignKey("CourseSection", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024, verbose_name="问题内容")
    enquiries_count = models.IntegerField(default=0, verbose_name="同问者计数")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="问题记录的截图等")
    date = models.DateTimeField(auto_now_add=True)
    status_choices = ((0, '待解答'), (1, '已解答'), (2, '已关闭'))
    status = models.SmallIntegerField(choices=status_choices, default=0)

    class Meta:
        verbose_name_plural = "800000002. 讨论区：课程提问"

    def __str__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if self.degree_course is None and self.course_section is None:
            raise ValueError("提的问题必须关联学位课程或具体课时！")

        super(Question, self).save(*args, **kwargs)


# 43
class Answer(models.Model):
    """问题解答"""
    question = models.ForeignKey("Question", verbose_name="问题", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="回答")
    account = models.ForeignKey("Account", verbose_name="回答者", on_delete=models.CASCADE)
    agree_number = models.IntegerField(default=0, verbose_name="点赞数")
    disagree_number = models.IntegerField(default=0, verbose_name="点踩数")
    answer_date = models.DateTimeField(auto_now=True, verbose_name="日期")

    class Meta:
        verbose_name_plural = "800000003. 讨论区：解答"

    def __str__(self):
        return "%s" % self.question


# 44
class AnswerComment(models.Model):
    """答案回复评论"""
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    reply_to = models.ForeignKey("self", blank=True, null=True, verbose_name="基于评论的评论", on_delete=models.CASCADE)
    comment = models.TextField(max_length=512, verbose_name="评论内容")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="跟进记录的截图等")
    account = models.ForeignKey("Account", verbose_name="评论者", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "800000004. 讨论区：评论"

    def __str__(self):
        return "%s - %s" % (self.account, self.comment)


# 45
class QACounter(models.Model):
    """ 问题和回答的赞同数量统计 """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    data_type_choices = ((0, '点赞'), (1, '踩'), (2, '同问'))
    data_type = models.SmallIntegerField(choices=data_type_choices)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "800000005. 问题和回答的赞同数量统计"
        unique_together = ("content_type", 'object_id', "account")

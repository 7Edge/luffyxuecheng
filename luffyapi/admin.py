from django.contrib import admin

# Register your models here.

from luffyapi import models

admin.site.register(models.CourseCategory)
admin.site.register(models.CourseSubCategory)
admin.site.register(models.DegreeCourse)
admin.site.register(models.Teacher)
admin.site.register(models.Scholarship)
admin.site.register(models.Course)
admin.site.register(models.CourseDetail)
admin.site.register(models.OftenAskedQuestion)
admin.site.register(models.CourseOutline)
admin.site.register(models.Chapters)
admin.site.register(models.CourseSection)
admin.site.register(models.HomeWork)
admin.site.register(models.HomeworkRecord)
admin.site.register(models.MentorGroup)
admin.site.register(models.CourseSchedule)
admin.site.register(models.StudyRecord)
admin.site.register(models.EnrolledDegreeCourse)
admin.site.register(models.DegreeRegistrationForm)
admin.site.register(models.EnrolledCourse)


admin.site.register(models.PricePolicy)
admin.site.register(models.UserInfo)
admin.site.register(models.UserToken)
admin.site.register(models.Account)
admin.site.register(models.Province)
admin.site.register(models.City)
admin.site.register(models.Industry)
admin.site.register(models.Profession)
admin.site.register(models.Feedback)
admin.site.register(models.ArticleSource)
admin.site.register(models.Article)
admin.site.register(models.Collection)
admin.site.register(models.Comment)
admin.site.register(models.Tags)


admin.site.register(models.ScoreRule)
admin.site.register(models.ScoreRecord)

admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)


admin.site.register(models.Order)
admin.site.register(models.OrderDetail)
admin.site.register(models.TransactionRecord)
admin.site.register(models.StuFollowUpRecord)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.AnswerComment)
admin.site.register(models.QACounter)




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
admin.site.register(models.PricePolicy)
admin.site.register(models.UserInfo)
admin.site.register(models.UserToken)
admin.site.register(models.ArticleSource)
admin.site.register(models.Article)
admin.site.register(models.Collection)
admin.site.register(models.Comment)
admin.site.register(models.Tags)

admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)

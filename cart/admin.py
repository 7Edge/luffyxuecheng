from django.contrib import admin

from luffyapi import models

# Register your models here.

site = admin.site
site.register(models.CourseCategory)
site.register(models.CourseSubCategory)
site.register(models.Teacher)
site.register(models.DegreeCourse)
site.register(models.UserInfo)
site.register(models.UserToken)
site.register(models.PricePolicy)

site.register(models.Coupon)
site.register(models.CouponRecord)

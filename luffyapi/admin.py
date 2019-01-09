from django.contrib import admin

# Register your models here.

from luffyapi import models


admin.site.register(models.Course)
admin.site.register(models.CourseDetail)
admin.site.register(models.Chapters)
admin.site.register(models.UserInfo)
admin.site.register(models.UserToken)

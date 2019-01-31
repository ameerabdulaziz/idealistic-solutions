from django.contrib import admin

from . import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Department)
admin.site.register(models.Role)
admin.site.register(models.Staff)

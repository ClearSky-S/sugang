from pickletools import StackObject

from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (("Student Info", {"fields": ("student",)}),)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Credits)
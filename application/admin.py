from django.contrib import admin
from utsida.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


admin.site.register(AbroadCourse)
admin.site.register(Case)
admin.site.register(Faculty)
admin.site.register(Institute)
admin.site.register(Country)
admin.site.register(University)



class HomeCourseAdmin(admin.ModelAdmin):
    search_fields = ('code',)

admin.site.register(HomeCourse,HomeCourseAdmin)


class CourseMatchAdmin(admin.ModelAdmin):
    search_fields = ('homeCourse', 'code',)
    raw_id_fields = ("homeCourse",)


admin.site.register(CourseMatch, CourseMatchAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'student'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User,UserAdmin)


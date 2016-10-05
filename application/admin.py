from django.contrib import admin
from utsida.models import *
# Register your models here.


admin.site.register(AbroadCourse)
admin.site.register(Case)
admin.site.register(Faculty)
admin.site.register(Institute)
admin.site.register(Continent)
admin.site.register(Country)


class HomeCourseAdmin(admin.ModelAdmin):
    search_fields = ('code',)

admin.site.register(HomeCourse,HomeCourseAdmin)


class CourseMatchAdmin(admin.ModelAdmin):
    search_fields = ('homeCourse', 'code',)
    raw_id_fields = ("homeCourse",)


admin.site.register(CourseMatch, CourseMatchAdmin)

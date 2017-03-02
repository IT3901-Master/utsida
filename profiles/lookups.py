from ajax_select import register, LookupChannel
from django.db.models import Q

from .models import *
from django.utils.six import text_type
from django.utils.html import escape

@register('homeCourse')
class CourseLookup(LookupChannel):

    model = Profile
    min_length = 3

    def check_auth(self, request):
        if request.user.is_authenticated():
            return True

    def get_query(self, q, request):
        return HomeCourse.objects.filter(Q(name__icontains=q) | Q(code__istartswith=q)).order_by('name')[:10]

    def get_result(self, obj):
        return text_type(obj.name)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return "<span class="">%s, %s </span>" % (escape(obj.code), escape(obj.name))



@register('singleHomeCourse')
class singleHomeCourse(LookupChannel):

    model = Profile
    min_length = 3

    def check_auth(self, request):
        if request.user.is_authenticated():
            return True

    def get_query(self, q, request):
        return HomeCourse.objects.filter(Q(name__icontains=q) | Q(code__istartswith=q)).order_by('name')[:10]

    def get_result(self, obj):
        return text_type(obj.code) + " - " + text_type(obj.name)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return "<span class="">%s, %s </span>" % (escape(obj.code), escape(obj.name))


@register('institute')
class InstituteLookup(LookupChannel):

    model = Institute
    min_length = 1

    def check_auth(self, request):
        if request.user.is_authenticated():
            return True

    def get_query(self, q, request):
        return Institute.objects.all().filter(Q(name__icontains=q) | Q(acronym__icontains=q)).order_by('name')[:10]

    def get_result(self, obj):
        return text_type(obj.acronym) + " - " + text_type(obj.name)

    def format_match(self, obj):
        return self.format_item_display(obj.name)
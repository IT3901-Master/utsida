from ajax_select import register, LookupChannel
from django.db.models import Q

from .models import *
from django.utils.six import text_type
from django.utils.html import escape

@register('homeCourseFind')
class CourseFindChannel(LookupChannel):

    model = CourseMatch
    min_length = 3

    def check_auth(self, request):
        if request.user.is_authenticated():
            return True

    def get_query(self, q, request):
        return HomeCourse.objects.filter(Q(name__icontains=q) | Q(code__istartswith=q)).order_by('name')

    def get_result(self, obj):
        return text_type(obj.name)

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return "<span class="">%s, %s </span>" % (escape(obj.code), escape(obj.name))
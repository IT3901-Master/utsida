from django import template
from django.contrib.auth.models import Group
from django.shortcuts import redirect

register = template.Library()


@register.filter
def get(d, key):
    return d[key]

@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

@register.filter
def parse_similarity(value, arg):
    return '%.0f' % (float(value) * arg) + '%'

from django import template

register = template.Library()


@register.filter
def get(d, key):
    return d[key]

@register.filter
def parse_similarity(value, arg):
    return '%.0f' % (float(value) * arg) + '%'

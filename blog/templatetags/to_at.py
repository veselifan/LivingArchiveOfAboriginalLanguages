from django import template

register = template.Library()

@register.filter
def to_at(value):
    return value.replace("@"," at ")
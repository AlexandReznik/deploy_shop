from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def email_to_link_2(value):
    return mark_safe(f"<a href='mailto:{value}' style='font-weight: 300; font-size: 16px; line-height: 26px; letter-spacing: 0.04em; color: #1F3F68; opacity: 0.6;'>{value}</a>")

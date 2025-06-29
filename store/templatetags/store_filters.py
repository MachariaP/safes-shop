from django import template
from django.utils.safestring import mark_safe
import bleach

register = template.Library()

@register.filter
def safe_html(text):
    allowed_tags = ['p', 'b', 'i', 'u', 'strong', 'em', 'ul', 'ol', 'li', 'br', 'h1', 'h2', 'h3']
    return mark_safe(bleach.clean(text, tags=allowed_tags))

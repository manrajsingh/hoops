from django import template
import hashlib

register = template.Library()


@register.filter
def gravatar_url(email):
    return f'https://gravatar.com/avatar/{hashlib.md5(email.encode()).hexdigest()}'
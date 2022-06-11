from django import template # type: ignore

register = template.Library()

@register.simple_tag
def text_to_id(text):
    return text.replace(' ', '-').lower()